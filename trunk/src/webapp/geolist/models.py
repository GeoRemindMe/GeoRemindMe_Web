# coding=utf-8

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from geouser.models import User
from geouser.models_acc import UserTimelineSystem
from georemindme.models_utils import Visibility
from georemindme.decorators import classproperty
from models_indexes import ListFollowersIndex


class List(polymodel.PolyModel):
    '''
        NO USAR ESTA LISTA, USAR LOS MODELOS ESPECIFICOS :D
    '''
    name = db.StringProperty()
    description = db.TextProperty()
    keys = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)
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

    def _post_put(self):
        pass
    
    def put(self, *kwargs):
        self._pre_put()
        super(List, self).put(*kwargs)
        self._post_put()

#  from http://blog.notdot.net/2010/04/Pre--and-post--put-hooks-for-Datastore-models
old_put = db.put

def hooked_put(models, **kwargs):
  for model in models:
    if isinstance(model, List):
      model._pre_put()
  old_put(models, **kwargs)
  for model in models:
    if isinstance(model, List):
      model._post_put()

db.put = hooked_put

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
                    timeline = UserTimelineSystem(user=key, msg_id=352, instance=self)
                    timeline.put()
            return True


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
        timeline = UserTimelineSystem(user=self.user.key(), msg_id=251, instance=list)
        put = db.put_async(timeline, self)
        put.get_result()
        
    def put(self):
        if not self.is_saved():
            super(ListAlert, self).put()
            timeline = UserTimelineSystem(user=user.key(), msg_id=250, instance=list)
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
        timeline = UserTimelineSystem(user=self.user.key(), msg_id=151, instance=list)
        put = db.put_async(timeline, self)
        put.get_result()
        
    def put(self):
        if not self.is_saved():
            super(ListAlert, self).put()
            timeline = UserTimelineSystem(user=user.key(), msg_id=150, instance=list)
            timeline.put()
        else:
            super(ListAlert, self).put()
        
from helpers import *