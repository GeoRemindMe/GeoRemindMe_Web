# coding=utf-8

from django.conf import settings
from google.appengine.ext import db

from models import Event, Alert, AlertSuggestion, Suggestion
from exceptions import ForbiddenAccess
from geouser.models import User
from georemindme.paging import *
import memcache


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
        '''
        Obtiene un evento por su id, COMPRUEBA VISIBILIDAD, solo obtiene los publicos
        '''
        event = memcache.deserialize_instances(memcache.get('%sEVENT%s' % (memcache.version, id)), _search_class=self._klass)
        if event is None:
            event = self._klass.get_by_id(int(id))
            if not hasattr(event, '_vis'):
                return None
            if not event._is_public():
                return None
            memcache.set('%sEVENT%s' % (memcache.version, id), memcache.serialize_instances(event))
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
        if event.user.key() == user.key():
            return event
        return None
    
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
        if event.user.key() == user.key():
            return event
        elif hasattr(event, '_vis'):
            if event._is_public():
                return event
            elif event._is_shared() and event.user_invited(user):
                return event
        raise None
    
    def get_by_last_sync(self, user, last_sync):
        '''
        Obtiene los ultimos eventos a partir
        de una fecha de ultima sincronizacion
        '''
        if not isinstance(user, User):
            raise TypeError()
        return Alert.all().filter('user =', user).filter('modified >', last_sync).order('-modified')

    
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

