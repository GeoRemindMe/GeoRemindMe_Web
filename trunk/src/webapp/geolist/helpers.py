# coding=utf-8

from geouser.models import User
from models import *
from models_indexes import ListFollowersIndex

class ListHelper(object):
    _klass = List
    
    def get_by_id(self, id):
        return self._klass.get_by_id(id)
    
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
    

class ListAlertHelper(object):
    _klass = ListAlert
    

class ListUserHelper(object):
    _klass = ListUser
