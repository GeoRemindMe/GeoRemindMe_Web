# coding=utf-8

from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from geouser.models import User
from geouser.models_acc import UserTimelineSystem
from georemindme.models_utils import Visibility, HookedModel
from georemindme.models_indexes import Invitation
from georemindme.decorators import classproperty
from models_indexes import ListFollowersIndex
from signals import *


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
    
    _new = False
    
    @property
    def id(self):
        return self.key().id()
    
    @classproperty
    def objects(self):
        return ListHelper()

    def _pre_put(self):
        self.count = len(self.keys)
        if not self.is_saved():
            self._new = True
            
    def _post_put_sync(self):
        if self._new:
            list_new.send(sender=self)
            self._new = False
        else:
            if not self.active:
                list_deleted.send(sender=self)
            else:
                list_modified.send(sender=self)
       
    def to_dict(self):
            return {'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'user': self.user.username,
                    'modified': self.modified if self.modified is not None else 0,
                    'created': self.created if self.created is not None else 0,
                    'keys': [i.id() for i in self.keys], 
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
    def insert_list(cls, user, id=None, name=None, description = None, instances=[], vis='public'):
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
        list = None
        if id is not None:
            list = cls.objects.get_by_id_user(id, user)
        if list is None:
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
        self.put()
        
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
        db.run_in_transaction(_tx, index.key(), user_key)
        list_following_deleted.send(sender=self, user=db.get(user_key)) #  FIXME: recibir usuario como parametro
    
    def add_follower(self, user):
        '''
        Añade un usuario a los seguidores de una lista
        
            :param user: Usuario que quiere apuntarse a una sugerencia
            :type user: :class:`geouser.models.User`
            
            :returns: True si se añadio, False en caso contrario    
        '''
        if self._user_is_follower(user.key()):
            return True
        if self._is_private():
            return False
        elif self._is_shared():
            if self.user_invited(user) is None:
                return False   
        def _tx(list_key, user_key):
            # TODO : cambiar a contador con sharding
            list = db.get(list_key)
            if ListFollowersIndex.all().ancestor(list).filter('keys =', user_key).count() != 0:
                return  # el usuario ya sigue la lista
            list += 1
            # indice con personas que siguen la sugerencia
            index = ListFollowersIndex.all().ancestor(list).filter('count < 80').get()
            if index is None:
                index = ListFollowersIndex(parent=list)
            index.keys.append(user_key)
            index.count += 1
            db.put_async([list, index])
        db.run_in_transaction(_tx, list_key = self.key(), user_key = user.key())
        self.user_invited(user, set_status=1)  # FIXME : mejor manera de cambiar estado invitacion
        list_following_new.send(sender=self, user=user)
        return True
                
    def user_invited(self, user, set_status=None):
        '''
        Comprueba que un usuario ha sido invitado a la lista
            
            :param user: Usuario que debe estar invitado
            :type user: :class:`geouser.models.User`
            :param set_status: Nuevo estado para la invitacion
            :type set_status: :class:`integer`
            
            :returns: True si esta invitado, False en caso contrario
        '''
        invitation = Invitation.objects.is_user_invited(self, user)
        if invitation is not None and set_status is not None:
            invitation.set_status(set_status)
        return invitation


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
        self.put()

        
class ListUser(List):
    '''
    Lista agrupando usuarios, para mejor gestion del usuario, no es publica
    '''
    user = db.ReferenceProperty(User)
    
    @classproperty
    def objects(self):
        return ListUserHelper()
    
    @classmethod
    def insert_list(cls, user, name, description=None, instances=[]):
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
        list = user.listuser_set.filter('name =', name).get()
        if list is not None:
            if  description is not None:
                list.description = description
            keys = set(list.keys)
            keys |= set([instance.key() for instance in instances])
            list.keys = [k for k in keys]
            list.put()
            return list
        keys= set([instance.key() for instance in instances])
        list = ListUser(name=name, user=user, description=description, keys=[k for k in keys])
        list.put()
        return list
    
    def update(self, name=None, description=None, instances_add=[], instances_del=[]):
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
        self.put()
        


from watchers import *    
from helpers import *