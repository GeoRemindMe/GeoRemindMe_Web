# coding=utf-8

from google.appengine.ext import db

from models import Event, Alert, AlertSuggestion, Suggestion
from exceptions import ForbiddenAccess
from geouser.models import User
from georemindme.paging import PagedQuery
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
        from georemindme.funcs import prefetch_refprops
        events = p.fetch_page(page)
        events = prefetch_refprops(events, self._klass.user, self._klass.poi)
        return [p.id, events, p.page_count()]

    def get_by_id(self, id):
        '''
        Obtiene un evento por su id, COMPRUEBA VISIBILIDAD, solo obtiene los publicos
        '''
        try:
            id = int(id)
        except:
            raise TypeError
        event = memcache.deserialize_instances(memcache.get('%sEVENT%s' % (memcache.version, id)), _search_class=self._klass)
        if event is None:
            event = self._klass.get_by_id(int(id))
            if not hasattr(event, '_vis'):
                return None
            if not event._is_public():
                return None
            memcache.set('%sEVENT%s' % (memcache.version, id), memcache.serialize_instances(event),300)
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

    def get_by_id_user(self, id, user, querier):
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
        return None

    def get_by_id_querier(self, id, querier):
        '''
        Obtiene el evento con ese id comprobando que
        el usuario tiene acceso a el

            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(querier, User):
            raise TypeError()
        event = self.get_by_id(id)
        if event is None:
            return None
        if event.user is not None:
            if event.user.key() == querier.key():
                return event
        if hasattr(event, '_vis'):
            if event._is_public():
                return event
            elif event._is_shared() and event.user_invited(querier):
                return event
        return None

    def get_by_tag_querier(self, tagInstance, querier, page=1, query_id=None):
        if not isinstance(querier, User):
            raise TypeError()
        from geotags.models import Tag
        if not isinstance(tagInstance, Tag):
            raise TypeError
        events = self._klass.all().filter('_tags_list =', tagInstance.key())
        p = PagedQuery(events, id = query_id)
        events_lists = []
        from georemindme.funcs import prefetch_refprops
        events = p.fetch_page(page)
        events = prefetch_refprops(events, self._klass.user, self._klass.poi)
        for event in events:
            if event.user.key() == querier.key():
                events_lists.append(event)
            elif hasattr(event, '_vis'):
                if event._is_public():
                    events_lists.append(event)
                elif event._is_shared() and event.user_invited(querier):
                    events_lists.append(event)
        if len(events_lists) != 0:
            return [p.id, events_lists]
        return None

    def get_by_tag_owner(self, tagInstance, owner, page=1, query_id=None):
        if not isinstance(owner, User):
            raise TypeError()
        from geotags.models import Tag
        if not isinstance(tagInstance, Tag):
            raise TypeError
        events = self._klass.all().filter('_tags_list =', tagInstance.key()).filter('user =', owner)
        p = PagedQuery(events, id = query_id)
        from georemindme.funcs import prefetch_refprops
        events = p.fetch_page(page)
        events = prefetch_refprops(events, self._klass.user, self._klass.poi)
        return [p.id, events]

    def get_by_last_sync(self, user, last_sync):
        '''
        Obtiene los ultimos eventos a partir
        de una fecha de ultima sincronizacion
        '''
        if not isinstance(user, User):
            raise TypeError()
        return self._klass.all().filter('user =', user).filter('modified >', last_sync).order('-modified').fetch(50)


class AlertHelper(EventHelper):
    _klass = Alert

    def get_by_id_user(self, id, user):
        '''
        Obtiene el evento con ese id comprobando que
        pertenece al usuario

            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(user, User):
            raise TypeError()
        try:
            id = long(id)
        except:
            return None
        event = self._klass.get_by_id(int(id))
        if event is None:
            return None
        if event.user.key() == user.key():
                return event
        return None

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

    def get_by_slug_querier(self, slug, querier):
        '''
        Obtiene un evento por su id, COMPRUEBA VISIBILIDAD, solo obtiene los publicos
        '''
        suggestion = memcache.deserialize_instances(memcache.get('%sEVENT%s' % (memcache.version, slug)), _search_class=self._klass)
        if suggestion is None:
            suggestion = self._klass.all().filter('slug =', slug).get()
            if suggestion is None:
                suggestion = self.get_by_id(slug)
            if suggestion is not None:
                if suggestion._is_private():
                    if not querier.is_authenticated():
                        return None
                    if suggestion.user.key() != querier.key():
                        return None
                elif suggestion._is_shared():
                    if not querier.is_authenticated():
                        return None
                    if not suggestion.user_invited(querier):
                        return None
                memcache.set('%sEVENT%s' % (memcache.version, slug), memcache.serialize_instances(suggestion),300)
                return suggestion
        return suggestion

    def get_by_user(self, user, querier, page = 1, query_id = None):
        """
        Obtiene una lista con todos los Eventos
        de un usuario
        """
        if not isinstance(user, User) or not isinstance(querier, User):
            raise TypeError()
        if user.id == querier.id:
            q = self._klass.gql('WHERE user = :1 ORDER BY modified DESC', user)
        else:
            q = self._klass.gql('WHERE user = :1 AND _vis = :2 ORDER BY modified DESC', user, 'public')
        p = PagedQuery(q, id = query_id)
        suggestions = p.fetch_page(page)
        from georemindme.funcs import prefetch_refprops
        suggestions = prefetch_refprops(suggestions, self._klass.user, self._klass.poi)
        from geolist.models import ListSuggestion
        for s in suggestions:
            lists = ListSuggestion.objects.get_by_suggestion(s, querier)
            setattr(s, 'lists', lists)
        return [p.id, suggestions, p.page_count()]

    def get_by_place(self, place, page=1, query_id=None, async=False, querier=None):
        if querier is None:
            raise TypeError()
        q = self._klass.all().filter('poi =', place.key())
        p = PagedQuery(q, id = query_id)
        if async:
            return p.id, q.run()
        else:
            from geovote.models import Vote
            from georemindme.funcs import prefetch_refprops
            suggestions = p.fetch_page(page)
            suggestions = prefetch_refprops(suggestions, Suggestion.user, Suggestion.poi)
            [p.id, [{'instance': suggestion,
                     'has_voted':  Vote.objects.user_has_voted(querier, suggestion.key()),
                     'vote_counter': Vote.objects.get_vote_counter(suggestion.key())
                     } for suggestion in suggestions]
             ]

    def get_by_id_user(self, id, user, querier):
        '''
        Obtiene el evento con ese id comprobando que
        pertenece al usuario

            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(user, User) or not isinstance(querier, User):
            raise TypeError()
        event = self.get_by_id(id)
        if event is None:
            return None
        from geolist.models import ListSuggestion
        if event.user is None:
            return None
        if event.user.key() == user.key():
            if user.key() == querier.key():
                lists = ListSuggestion.objects.get_by_suggestion(event, querier)
                setattr(event, 'lists', lists)
                return event
            if event._is_public():
                lists = ListSuggestion.objects.get_by_suggestion(event, querier)
                setattr(event, 'lists', lists)
                return event
            elif event._is_shared() and event.user_invited(querier):
                lists = ListSuggestion.objects.get_by_suggestion(event, querier)
                setattr(event, 'lists', lists)
                return event
        return None

    def get_by_id_querier(self, id, querier):
        '''
        Obtiene el evento con ese id comprobando que
        el usuario tiene acceso a el

            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(querier, User):
            raise TypeError()
        event = self.get_by_id(id)
        if event is None:
            return None
        from geolist.models import ListSuggestion
        if event.user.key() == querier.key():
            lists = ListSuggestion.objects.get_by_suggestion(event, querier)
            setattr(event, 'lists', lists)
            return event
        if event._is_public():
            lists = ListSuggestion.objects.get_by_suggestion(event, querier)
            setattr(event, 'lists', lists)
            return event
        elif event._is_shared() and event.user_invited(querier):
            lists = ListSuggestion.objects.get_by_suggestion(event, querier)
            setattr(event, 'lists', lists)
            return event
        return None

    def get_by_user_following(self, user, page=1, query_id=None, async=False):
        if not isinstance(user, User):
            raise TypeError
        from models_indexes import SuggestionFollowersIndex
        q = SuggestionFollowersIndex.all().filter('keys =', user.key())
        p = PagedQuery(q, id = query_id)
        if async:
            return p.id, q.run()
        from georemindme.funcs import fetch_parents
        suggestions = fetch_parents(p.fetch_page(page))
        return [p.id, suggestions]
    
    def load_suggestions_by_user_following(self, query_id, suggestions):
        from georemindme.funcs import fetch_parents
        suggestions = fetch_parents(suggestions)
        return [query_id, suggestions]
    
    def get_nearest(self, location, radius = 5000, querier=None):
        if not isinstance(location, db.GeoPt):
            location = db.GeoPt(location)
        import memcache
        client = memcache.mem.Client()
        sugs = client.gets('%ssug_nearest%s,%s' % (memcache.version,
                                                   location.lat,
                                                   location.lon
                                                   ))
        if sugs is None:
            from mapsServices.fusiontable import ftclient, sqlbuilder
            
            ftclient = ftclient.OAuthFTClient()
            from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global
            query = ftclient.query(sqlbuilder.SQL().select(__web_settings.FUSIONTABLES['TABLE_SUGGS'], cols=['sug_id'],
                                                   condition = 'ST_INTERSECTS (location, CIRCLE(LATLNG (%s), %s)) ORDER BY modified LIMIT 8' % (location, radius)
                                                   )
                           )
            results = query.splitlines()
            del results[0] #  quitar la primera linea con el nombre de la columna
            sugs = [db.Key.from_path(self._klass.kind(), int(result)) for result in results] # construir todas las keys para consultar en bach
            from google.appengine.api import datastore
            sugs = datastore.Get(sugs)
            from georemindme.funcs import prefetch_refpropsEntity
            prefetch = prefetch_refpropsEntity(sugs, 'user')
            sugs = [{'id': sug.key().id(),
                     'slug': sug['slug'],
                     'username': prefetch[sug['user']].username,
                     'name': sug['name'],
                     'description': sug['description']} for sug in sugs]
            client.set('%ssug_nearest%s,%s' % (memcache.version,
                                                   location.lat,
                                                   location.lon
                                                   ), sugs, 1123)
            # FIXME : DEBERIA USARSE CAS EN VEZ DE SET EN MEMCACHE
        return sugs


class AlertSuggestionHelper(AlertHelper):
    _klass = AlertSuggestion

    def get_by_sugid_user(self, sugid, user):
        if not isinstance(user, User):
            raise TypeError()
        try:
            sugid = long(sugid)
        except:
            return None
        sugkey = db.Key.from_path(Suggestion.kind(), sugid)
        return self._klass.all().filter('suggestion =', sugkey).filter('user =', user).get()
