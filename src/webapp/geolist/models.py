# coding=utf-8

from django.utils import simplejson
from google.appengine.ext import db

from geouser.models import User
from georemindme.models_utils import Visibility, HookedModel
from georemindme.decorators import classproperty
from models_indexes import ListCounter


class List(db.polymodel.PolyModel, HookedModel):
    '''
        NO USAR ESTA LISTA, USAR LOS MODELOS ESPECIFICOS :D
    '''
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    keys = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add = True)
    modified = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    count = db.IntegerProperty(default=0)  # numero de sugerencias en la lista

    _counters = None
    _new = False

    @property
    def id(self):
        return self.key().id()

    @property
    def counters(self):
        if self._counters is None:
            self._counters = ListCounter.all().ancestor(self).get()
        return self._counters

    @classproperty
    def objects(self):
        return ListHelper()

    def _pre_put(self):
        self.count = len(self.keys)
        if not self.is_saved():
            self._new = True

    def _post_put_sync(self, **kwargs):
        if self._new:
            counter = ListCounter(parent=self)
            counter.put()
            list_new.send(sender=self)
            self._new = False
        else:
            if not self.active:
                list_deleted.send(sender=self)
            else:
                list_modified.send(sender=self)

    def to_dict(self, resolve=False):
            dict = {'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'user': self.user.username,
                    'modified': self.modified if self.modified is not None else 0,
                    'created': self.created if self.created is not None else 0,
                    'count': self.count, 
                    'counters': self.counters.to_dict(), 
                    'keys': [i.id() for i in self.keys],
                    }
            if resolve:
                dict['instances'] = db.get(self.keys)
            return dict

    def to_json(self):
        from libs.jsonrpc.jsonencoder import JSONEncoder
        return simplejson.dumps(self.to_dict(), cls=JSONEncoder)

    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return self.name


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
        from models_indexes import ListFollowersIndex
        index = ListFollowersIndex.all().ancestor(self.key()).filter('keys =', user_key).get()
        if index is not None:
            return True
        return False

    def notify_followers(self):
        '''
        Crea un timelineSystem por cada usuario que sigue
        a esta lista
        '''
        from models_indexes import ListFollowersIndex
        if not self._is_private():
            if ListFollowersIndex.all().ancestor(self.key()).count() == 0:
                return True
            for list in ListFollowersIndex.all().ancestor(self.key()):
                for key in list.users:
                    timeline = UserTimelineSystem(user=self.user, msg_id=351, instance=self)
                    timeline.put()
            return True

    @classmethod
    def insert_list(cls, user, id=None, name=None, description = None, instances=[], instances_del=[], vis='public'):
        """
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
        """
        from geoalert.models import Suggestion
        list = None
        if id is not None:
            list = cls.objects.get_by_id_user(id, user)
        if list is None:
            list = user.listsuggestion_set.filter('name =', name).get()
        if list is not None:  # la lista con ese nombre ya existe, la editamos
            list.update(name=name, description=description, instances=instances, instances_del=instances_del, vis=vis )
            return list
        # TODO: debe haber una forma mejor de quitar repetidos, estamos atados a python2.5 :(, los Sets
        keys= set([db.Key.from_path('Event', int(instance)) for instance in instances])
        list = ListSuggestion(name=name, user=user, description=description, keys=[k for k in keys], _vis=vis)
        list.put()
        return list

    def update(self, name=None, description=None, instances=[], instances_del=[], vis='public'):
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
        from geoalert.models import Suggestion
        if name is not None or name == '':
            self.name = name
        if description is not None:
            self.description = description
        for deleted in instances_del:
            try:
                self.keys.remove(db.Key.from_path('Event', int(deleted)))
            except:
                pass
        keys = set(self.keys)
        keys |= set([db.Key.from_path('Event', int(instance)) for instance in instances])
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
        from models_indexes import ListFollowersIndex
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
            from models_indexes import ListFollowersIndex
            if ListFollowersIndex.all().ancestor(list_key).filter('keys =', user_key).count() != 0:
                return True  # el usuario ya sigue la lista
            # indice con personas que siguen la sugerencia
            index = ListFollowersIndex.all().ancestor(list_key).filter('count <', 80).get()
            if index is None:
                index = ListFollowersIndex(parent=list_key)
            index.keys.append(user_key)
            index.count += 1
            index.put()
        tx = db.run_in_transaction(_tx, list_key = self.key(), user_key = user.key())
        if tx:
            return True
        self.user_invited(user, set_status=1)  # FIXME : mejor manera de cambiar estado invitacion
        list_following_new.send(sender=self, user=user)
        return True

    def has_follower(self, user):
        if not user.is_authenticated():
            return False
        if ListFollowersIndex.all().ancestor(self.key()).filter('keys =', user.key()).get() is not None:
            return True
        return False

    def delete(self):
        list_deleted.send(sender=self)
        super(ListSuggestion, self).delete()


class ListRequested(ListSuggestion):
    @classproperty
    def objects(self):
        return ListRequestedHelper()

    @classmethod
    def insert_list(cls, user, id=None, name=None, description = None, instances=[], instances_del=[], vis='public'):
        """
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
        """
        from geoalert.models import Suggestion
        list = None
        if id is not None:
            list = cls.objects.get_by_id_user(id, user)
        if list is None:
            list = user.listsuggestion_set.filter('name =', name).get()
        if list is not None:  # la lista con ese nombre ya existe, la editamos
            list.update(name=name, description=description, instances=instances, instances_del=instances_del, vis=vis )
            return list
        # TODO: debe haber una forma mejor de quitar repetidos, estamos atados a python2.5 :(, los Sets
        keys= set([db.Key.from_path('Event', int(instance)) for instance in instances])
        list = ListSuggestion(name=name, user=user, description=description, keys=[k for k in keys], _vis=vis)
        list.put()
        return list

    def update(self, querier, name=None, description=None, instances=[], instances_del=[], vis='public'):
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
        from geoalert.models import Suggestion
        if querier.key() == self.user.key():
            if name is not None or name == '':
                self.name = name
            if description is not None:
                self.description = description
            for deleted in instances_del:
                try:
                    self.keys.remove(db.Key.from_path('Event', int(deleted)))
                except:
                    pass
        else:
            invitation = self.user_invited(querier)
            if invitation is None or not invitation.is_accepted():
                from georemindme.exceptions import ForbiddenAccess
                raise ForbiddenAccess
        keys = set(self.keys)
        keys |= set([db.Key.from_path('Event', int(instance)) for instance in instances])
        self.keys = [k for k in keys]
        self._vis = vis
        self.put(querier=querier)

        def _post_put_sync(self, querier, **kwargs):
            if self._new:
                counter = ListCounter(parent=self)
                counter.put()
                list_new.send(sender=self)
                self._new = False
            else:
                if not self.active:
                    list_deleted.send(sender=self)
                else:
                    list_modified.send(sender=self, querier=querier)


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
        """
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
        """
        from geoalert.models import Alert
        list = user.listalert_set.filter('name =', name).get()
        if list is not None:  # la lista con ese nombre ya existe, la editamos
            if description is not None:
                list.description = description
            keys = set(list.keys)
            keys |= set([db.Key.from_path('Event', int(instance)) for instance in instances])
            list.keys = [k for k in keys]
            list.put()
            return list
        # TODO: debe haber una forma mejor de quitar repetidos, estamos atados a python2.5 :(, los Sets
        keys= set([db.Key.from_path('Event', int(instance)) for instance in instances])
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

class _Deleted_List(db.Model):
    # TODO: crear deleted list
    pass

from watchers import *
from helpers import *
