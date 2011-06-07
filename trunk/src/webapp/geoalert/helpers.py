# coding=utf-8

from django.conf import settings
from google.appengine.ext import db

from models import Event, Alert, AlertSuggestion, Suggestion
from exceptions import ForbiddenAccess
from geouser.models import User
from georemindme.paging import *


class EventHelper(object):
    ''' Clase Helper para realizar busquedas en el datastore '''
    _klass = Event
        
    def get_by_user(self, user, page = 1, query_id = None):
        '''
        Obtiene una lista con todos los Eventos
        de un usuario
        '''
        if not isinstance(user, User):
            raise TypeError()
        q = self._klass.gql('WHERE user = :1 ORDER BY modified DESC', user)
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id(self, id):
        event = memcache.deserialize_instances(memcache.get('%sEVENT%s' % (memcache.version, id)))
        if event is None:
            event = self._klass.objects.get_by_id(id)
            memcache.set('%sEVENT%s' % (memcache.version, id), memcache.serialize_instances(suggestion))
        return event     
    
    def get_by_key(self, key):
        '''
        Obtiene el evento con ese key
        '''
        return self._klass.get(key)
    
    def get_by_key_user(self, key, user):
        '''
        Obtiene el evento con ese key y comprueba que
        pertenece a un usuario
        
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(user, User):
            raise TypeError()
        event = self._klass.get(key)
        if event is None:
            return None
        if event.user.key() != user.key():
            raise ForbiddenAccess()
        return event
    
    def get_by_id_user(self, id, user):
        '''
        Obtiene el evento con ese id comprobando que
        pertenece al usuario
        
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(user, User):
            raise TypeError()
        event = self._klass.get_by_id(int(id))
        if event is None:
            return None
        if event.user.key() != user.key():
            raise ForbiddenAccess()
        return event
    
    def get_by_last_sync(self, user, last_sync):
        '''
        Obtiene los ultimos eventos a partir
        de una fecha de ultima sincronizacion
        '''
        if not isinstance(user, User):
            raise TypeError()
        return None

    
class AlertHelper(EventHelper):
    _klass = Alert
    
    def get_by_user_done(self, user, page=1, query_id=None):
        '''
        Obtiene una lista con todos los Eventos
        de un usuario
        '''
        if not isinstance(user, User):
            raise TypeError()
        q = self._klass.gql('WHERE user = :1 AND has = "done:T" ORDER BY modified DESC', user)
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
        
        
    def get_by_user_undone(self, user, page=1, query_id=None):
        '''
        Obtiene una lista con todos los Eventos
        de un usuario
        '''
        if not isinstance(user, User):
            raise TypeError()
        q = self._klass.gql('WHERE user = :1 AND has = "done:F" ORDER BY modified DESC', user)
        return [l for l in q]
    

class SuggestionHelper(EventHelper):
    _klass = Suggestion


class AlertSuggestionHelper(AlertHelper):
    _klass = AlertSuggestion

