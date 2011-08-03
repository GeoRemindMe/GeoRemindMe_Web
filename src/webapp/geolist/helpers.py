# coding=utf-8

from geouser.models import User
from models import *
from models_indexes import ListFollowersIndex

class ListHelper(object):
    _klass = List
    
    def get_all_public(self, query_id=None, page=1):
        '''
        Devuelve todas las listas publicas ¡PAGINADA!
        
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
        '''            
        q = self._klass.all().filter('_vis =', 'public').order('-modified')
        from georemindme.paging import PagedQuery
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_user(self, user, query_id=None, page=1):
        '''
        Devuelve todas las listas del usuario ¡PAGINADA!
        Si usuario es None y la lista es publica, tambien devuelve la lista
        
            :param user: identificador del usuario
            :type user: :class:`geouser.models.User`
            :returns: [query_id, [:class:`geolist.models.ListUser`]
        '''
        if not isinstance(user, User):
            raise TypeError()
        q = self._klass.gql('WHERE user = :1 ORDER BY modified DESC', user)
        from georemindme.paging import PagedQuery
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id(self, id):
        '''
        Devuelve la lista publica con ese ID
        
            :param id: identificador de la lista
            :type id: :class:`Integer`
            :returns: None o :class:`geolist.models.List`
        '''
        try:
            id = int(id)
        except:
            raise TypeError
        list = self._klass.get_by_id(id)
        return None
    
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
            elif hasattr(list, '_vis'):
                if list._is_public():
                    return list
                elif user is not None and list._is_shared() and list.user_invited(user):
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
    
    def get_shared_list(self, user):
        '''
        Devuelve las listas que el usuario tiene invitacion
        
            :param user: usuario del que buscar las listas
            :type user: :class:`geouser.models.User`
        '''
        lists = [inv.list for inv in user.toinvitations_set if inv.status == 1]
    
    
class ListSuggestionHelper(object):
    _klass = ListSuggestion
    
    def get_by_name_user(self, name, user):
        list = self._klass.all().filter('user =', user).filter('name =', name).get()
        if not list.active:
            return None
        return list
    
    def get_by_id_querier(self, id, querier):
        '''
        Devuelve la lista publica con ese ID
        
            :param id: identificador de la lista
            :type id: :class:`Integer`
            :returns: None o :class:`geolist.models.List`
        '''
        if not isinstance(querier, User):
            raise TypeError()
        list = self.get_by_id(id)
        if list is None:
            return None
        if list.user.key() == querier.key():
            return list
        if list._is_public():
            return list
        elif list._is_shared() and list.user_invited(querier):
            return list
        return None
    
        
    def get_by_user(self, user, querier, page = 1, query_id = None):
        """
        Obtiene las listas de un usuario
        """
        if not isinstance(user, User) or not isinstance(querier, User):
            raise TypeError()
        if user.id == querier.id:
            q = self._klass.gql('WHERE user = :1 ORDER BY modified DESC', user)
        else:
            q = self._klass.gql('WHERE user = :1 AND _vis = :2 ORDER BY modified DESC', user, 'public')
        from georemindme.paging import PagedQuery
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page), p.page_count()]
    

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
