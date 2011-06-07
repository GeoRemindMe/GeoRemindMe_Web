# coding=utf-8

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from geouser.models import User
from geouser.models_acc import UserTimelineSystem
from georemindme.models_utils import Visibility, HookedModel
from georemindme.decorators import classproperty
from models_indexes import ListFollowersIndex


class List(polymodel.PolyModel, HookedModel):
    '''
        NO USAR ESTA LISTA, USAR LOS MODELOS ESPECIFICOS :D
    '''
    name = db.StringProperty()
    description = db.TextProperty()
    keys = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    count = db.IntegerProperty()
    
    @property
    def id(self):
        return self.id()
    
    @classproperty
    def objects(self):
        return ListHelper()
    
    def _user_is_follower(self, user_key):
        '''
        Busca si un usuario ya sigue a una lista
        
            :param user_key: key del usuario a buscar
            :type user_key: :class:`db.Key`
            :returns: True si el usuario ya sigue la lista. False si no.
        '''
        if not self.is_saved():
            return db.NotSavedError()
        index = ListFollowersIndex.all().ancestor(self.key()).filter('keys =', user_key).get()
        if index is not None:
            return True
        return False
            
    def add_follower(self, user_key):
        '''
        Añade un usuario a la lista
        
            :param user_key: key del usuario a buscar
            :type user_key: :class:`db.Key`
            :returns: True si se añadio (o ya existia) el usuario. False si hubo algun error
        '''
        def _tx(index_key, user_key):
            index = db.get(index_key)
            index.keys.append(user_key)
            index.count += 1
            index.put()
        if self._user_is_follower(user_key):
            return True
        if ListFollowersIndex.all().ancestor(self.key).count() == 0:
            index = ListFollowersIndex(parent=self, kind=self.kind())
            index.put()
        else:
            index = ListFollowersIndex.all().ancestor(self.key()).filter('count <', 80).order('created').get()
        # TODO: en vez de cargar todo el objeto, obtener solo el key
        db.run_in_transaction(index.key(), user_key)
        
    def del_follower(self, user_key):
        '''
        Borra un usuario de la lista
        
            :param user_key: key del usuario a buscar
            :type user_key: :class:`db.Key`
            :returns: True si se borro el usuario. False si hubo algun error o no existia
        '''
        def _tx(index_key, user_key):
            index = db.get(index_key)
            index.keys.remove(user_key)
            index.count -= 1
            index.put()
        if not self._user_is_follower(user_key):
            return False
        index = ListFollowersIndex.all().ancestor(self.key()).filter('keys =', user_key).get()
        db.run_in_transaction(index.key(), user_key)
        
    def _pre_put(self):
        self.count = len(self.keys)
    
    def put(self, *kwargs):
        self._pre_put()
        super(List, self).put(*kwargs)
        self._post_put()
        
    def to_dict(self):
            return {'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'user': self.user.username,
                    'modified': unicode(self.modified.strftime("%d%b")),
                    'created': unicode(self.created.strftime("%d%b")),
                    'instances': [i.id() for i in self.instances], 
                    }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())

class ListSuggestion(List, Visibility):
    '''
    Lista agrupando sugerencias, que no tienen porque ser sugerencias
    creadas por el mismo usuario que crea la lista.
    Tiene control de visibilidad
    '''
    
    user = db.ReferenceProperty(User)
    
    @classproperty
    def objects(self):
        return ListSuggestionHelper()
    
    def notify_followers(self):
        '''
        Crea un timelineSystem por cada usuario que sigue
        a esta lista
        '''
        if not self._is_private():
            if ListFollowersIndex.all().ancestor(self.key()).count() == 0:
                return True
            for list in ListFollowersIndex.all().ancestor(self.key()):
                for key in list.users:
                    timeline = UserTimelineSystem(user=self.user, msg_id=351, instance=self)
                    timeline.put()
            return True
        
    @classmethod
    def insert_list(cls, user, name, description = None, instances=[], vis='public'):
        '''
        Crea una nueva lista, en el caso de que exista una con ese nombre,
        se añaden las alertas
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geoalert.models.Alert`
            :param vis: Visibilidad de la lista
            :type vis: :class:`string`
        '''
        list = user.listsuggestion_set.filter('name =', name).get()
        if list is not None:  # la lista con ese nombre ya existe, la editamos
            if description is not None:
                list.description = description
            keys = set(list.keys)
            keys |= set([instance.key() for instance in instances])
            list.keys = [k for k in keys]
            list._vis = vis
            list.put()
            return list
        # TODO: debe haber una forma mejor de quitar repetidos, estamos atados a python2.5 :(, los Sets
        keys= set([instance.key() for instance in instances])
        list = ListSuggestion(name=name, user=user, description=description, keys=[k for k in keys], _vis=vis)
        list.put()
        return list
    
    def update(self, name=None, description=None, instances_add=[], instances_del=[], vis='public'):
        '''
        Actualiza una lista de alertas
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geoalert.models.Alert`
            :param vis: Visibilidad de la lista
            :type vis: :class:`string`
        '''
        if name is not None:
            self.name = name
        if description is not None:
                self.description = description
        for instance in instances_del:
            try:
                self.keys.remove(instance.key())
            except ValueError:
                pass
        keys = set(self.keys)
        keys |= set([instance.key() for instance in instances_add])
        self.keys = [k for k in keys]
        self._vis = vis
        timeline = UserTimelineSystem(user=self.user.key(), msg_id=351, instance=self)
        put = db.put_async(timeline, self)
        put.get_result()
        
    def add_follower(self, user):
        '''
        Añade un usuario a los seguidores de una lista
        
            :param user: Usuario que quiere apuntarse a una sugerencia
            :type user: :class:`geouser.models.User`
            
            :returns: True si se añadio, False en caso contrario    
        '''
        if self._is_private():
            return False
        elif self._is_shared() and not self.user_invited():
            return False   
        def _tx(sug_key, user_key):
            # TODO : cambiar a contador con sharding
            list = db.get(key)
            if ListFollowersIndex.all().ancestor(list).filter('keys =', user_key).count() != 0:
                return  # el usuario ya sigue la lista
            list += 1
            # indice con personas que siguen la sugerencia
            index = ListFollowersIndex.all().ancestor(list).filter('count < 80').get()
            if index is None:
                index = ListFollowersIndex(parent=list)
            index.keys.append(user_key)
            index.count += 1
            # TODO : cambiar estado de invitacion
            db.put_async([list, index])
        db.run_in_transaction(_tx, sug_key = self.key(), user_key = user.key())
        return True
            
    def _pre_put(self):
        if self.is_saved():
            if not self.active:
                timeline = UserTimelineSystem(user=self.user, msg_id=352, instance=self)
                timeline.put()
            else:
                from georemindme.tasks import NotificationHandler
                NotificationHandler().list_followers_notify(self)
                
    def user_invited(self, user):
        '''
        Comprueba que un usuario ha sido invitado a la sugerencia
            
            :param user: Usuario que debe estar invitado
            :type user: :class:`geouser.models.User`
            
            :returns: True si esta invitado, False en caso contrario
        '''
        return Invitation.objects.get_user_invited(self, user)


class ListAlert(List):
    '''
    Lista agrupando alertas, las alertas nunca son visibles por otros
    usuarios
    '''
    user = db.ReferenceProperty(User)
    
    @classproperty
    def objects(self):
        return ListAlertHelper()
    
    @classmethod
    def insert_list(cls, user, name, description = None, instances=[]):
        '''
        Crea una nueva lista, en el caso de que exista una con ese nombre,
        se añaden las alertas
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geoalert.models.Alert`
        '''
        list = user.listalert_set.filter('name =', name).get()
        if list is not None:  # la lista con ese nombre ya existe, la editamos
            if description is not None:
                list.description = description
            keys = set(list.keys)
            keys |= set([instance.key() for instance in instances])
            list.keys = [k for k in keys]
            list.put()
            return list
        # TODO: debe haber una forma mejor de quitar repetidos, estamos atados a python2.5 :(, los Sets
        keys= set([instance.key() for instance in instances])
        list = ListAlert(name=name, user=user, description=description, keys=[k for k in keys])
        list.put()
        return list
    
    def update(self, name=None, description=None, instances_add=[], instances_del=[]):
        '''
        Actualiza una lista de alertas
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geoalert.models.Alert`
        '''
        if name is not None:
            self.name = name
        if description is not None:
                self.description = description
        for instance in instances_del:
            try:
                self.keys.remove(instance.key())
            except ValueError:
                pass
        keys = set(self.keys)
        keys |= set([instance.key() for instance in instances_add])
        self.keys = [k for k in keys]
        timeline = UserTimelineSystem(user=self.user.key(), msg_id=251, instance=self)
        put = db.put_async(timeline, self)
        put.get_result()
        
    def put(self):
        if not self.active:
                timeline = UserTimelineSystem(user=self.user, msg_id=252, instance=self)
                timeline.put()
        if not self.is_saved():
            super(ListAlert, self).put()
            timeline = UserTimelineSystem(user=self.user.key(), msg_id=250, instance=self)
            timeline.put()
        else:
            super(ListAlert, self).put()
        
class ListUser(List):
    '''
    Lista agrupando usuarios, para mejor gestion del usuario, no es publica
    '''
    user = db.ReferenceProperty(User)
    
    @classproperty
    def objects(self):
        return ListUserHelper()
    
    @classmethod
    def insert_list(cls, user, name, description=None, instances=None):
        '''
        Crea una nueva lista de usuarios, en el caso de que exista una con ese nombre,
        se añaden los usuarios
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geouser.models.User`
        '''
        list = user.listuser_set.filter('name =', name)
        if list is not None:
            if  description is not None:
                list.description = description
            keys = set(list.keys)
            keys |= set([instance.key() for instance in instances])
            list.keys = [k for k in keys]
        list = ListUser(name=name, user=user, description=description, keys=[k for k in keys])
        list.put()

        return list
    
    def update(self, name=None, description=None, instances_add=None, instances_del=None):
        '''
        Actualiza una lista de usuarios
        
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :param name: nombre de la lista
            :type name: :class:`string`
            :param description: descripcion de la lista
            :type description: :class:`string`
            :param instances: objetos a añadir a la lista
            :type instances: :class:`geouser.models.User`
        '''
        if name is not None:
            self.name = name
        if description is not None:
                self.description = description
        for instance in instances_del:
            try:
                self.keys.remove(instance.key())
            except ValueError:
                pass
        keys = set(self.keys)
        keys |= set([instance.key() for instance in instances_add])
        self.keys = [k for k in keys]
        timeline = UserTimelineSystem(user=self.user.key(), msg_id=151, instance=self)
        put = db.put_async(timeline, self)
        put.get_result()
        
    def put(self):
        if not self.active:
                timeline = UserTimelineSystem(user=self.user, msg_id=152, instance=self)
                timeline.put()
        if not self.is_saved():
            super(ListAlert, self).put()
            timeline = UserTimelineSystem(user=self.user.key(), msg_id=150, instance=list)
            timeline.put()
        else:
            super(ListAlert, self).put()
        
from helpers import *