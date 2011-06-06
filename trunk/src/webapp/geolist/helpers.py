# coding=utf-8

from geouser.models import User
from models import *
from models_indexes import ListFollowersIndex

class ListHelper(object):
    _klass = List
    
    def get_by_user(self, user, query_id=None, page=1):
        '''
        Devuelve todas las listas del usuario ¡PAGINADA!
        Si usuario es None y la lista es publica, tambien devuelve la lista
        
            :param user: identificador de la lista
            :type user: :class:`geouser.models.User`
            :returns: [query_id, [:class:`geolist.models.ListUser`]
        '''
        if not isinstance(user, User):
            raise TypeError()
        q = self._klass.gql('WHERE user = :1 ORDER BY modified DESC', user)
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id(self, id):
        '''
        Devuelve la lista con ese ID y el usuario. 
        Si usuario es None y la lista es publica, tambien devuelve la lista
        
            :param id: identificador de la lista
            :type id: :class:`Integer`
            :returns: None o :class:`geolist.models.List`
        '''
        return self._klass.get_by_id(id)
    
    def get_by_id_user(self, id, user = None):
        '''
        Devuelve la lista con ese ID y el usuario. 
        Si usuario es None y la lista es publica, tambien devuelve la lista
        
            :param id: identificador de la lista
            :type id: :class:`Integer`
            :param user: usuario
            :type user: :class:`geouser.models.User`
            :returns: None o :class:`geolist.models.List`
        '''
        # TODO : si la lista es 'shared', mirar si el usuario tiene visibilidad
        list = self._klass.get_by_id(id)
        if not list.active:
            return None
        if list is not None:
            if list.user == user:
                return list
            if list._is_public():
                return list
        return None
    
    def get_list_user_following(self, user):
        '''
        Devuelve las listas a las que sigue el usuario
                
            :param user: usuario del que buscar las listas
            :type user: :class:`geouser.models.User`
        '''
        indexes = ListFollowersIndex.all().filter('_kind =', self._klass.kind()).filter('keys =', user.key())
        return [index.parent() for index in indexes]
    
    
class ListSuggestionHelper(object):
    _klass = ListSuggestion
    
    def get_by_name_user(self, name, user):
        list = self._klass.all().filter('user =', user).filter('name =', name).get()
        if not list.active:
            return None
        return list
    

class ListAlertHelper(object):
    _klass = ListAlert
    
    def get_by_name_user(self, name, user):
        list = self._klass.all().filter('user =', user).filter('name =', name).get()
        if not list.active:
            return None
        return list
    

class ListUserHelper(object):
    _klass = ListUser
    
    def get_by_name_user(self, name, user):
        list = self._klass.all().filter('user =', user).filter('name =', name).get()
        if not list.active:
            return None
        return list
