# coding=utf-8

from datetime import datetime
import time

from django.utils.translation import gettext_lazy as _
from django.utils import simplejson
from google.appengine.ext import db, search
from google.appengine.ext.db import polymodel
from google.appengine.ext.db import BadValueError

from georemindme.models_utils import Visibility
from georemindme.decorators import classproperty
from geouser.models import User
from geotags.models import Taggable
from geouser.models_acc import UserTimelineSystem
from models_poi import *
from models_indexes import *
from exceptions import ForbiddenAccess
from signals import *
from watchers import *


class Event(polymodel.PolyModel, search.SearchableModel, Taggable):
    """Informacion comun para las alertas y recomendaciones"""
    

    #in the appengine datastore, is more eficient to use stringlistproperty than some booleanProperty, its only needs one index
    #I now alert only have 2 boolean by now, but is better to learn these things.  
    #see tip #6 and #7 -> http://googleappengine.blogspot.com/2009/06/10-things-you-probably-didnt-know-about.html
    has = None
    
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [[], 'name', 'description']
    
    @classproperty
    def objects(self):
        return EventHelper()
    
    @property
    def id(self):
        return int(self.key().id())

    '''
    def put(self):
        try:
            if self.date_ends < self.date_starts:
                raise BadValueError('date starts > date ends')
        except TypeError:
            pass
        except:
            raise
                
        super(polymodel.PolyModel, self).put()
    '''
    def is_active(self):
        if 'active:T' in self.has:
            return True
        return False
    
    def toggle_active(self):
        if self.is_active():
            self.has.remove(u'active:T')
            self.has.append('active:F')
            return False
        self.has.remove(u'active:F')
        self.has.append(u'active:T')
        return True
    
    def get_distance(self):       
        '''
            Returns the distance from which the user wants to be notified
            returns 0 if users wants to be notified at default
        '''
        d = self._get_value_from_has('distance:\d*')# search pattern: distance:numbers
        if d:
            return int(d)
        return 0 
    
    def set_distance(self, distance):
        '''
            Set a new distance from which the user wants to be notified
            returns 0 if users wants to be notified at default
        '''
        try:
            d = self.get_distance()# get the distance
            self.has.remove(u'distance:%d' % int(d)) #remove the actual distance
        except:
            pass
        self.has.append(u'distance:%d' % distance)#adds the new distance
        return True
    
    def _get_value_from_has(self, pattern):
        '''
            Search in has using the pattern
        '''
        import re
        hastemp = ' '.join([i for i in self.has])# convert string list in one string
        r = re.compile(pattern)#create pattern
        result = r.search(hastemp)
        if result:
            tmp = result.group(0)#only one group have to be matched
            tmp = tmp.split(':')[1]
            if tmp == 'T':
                return True
            elif tmp == 'F':
                return False  
            return tmp   
        return None
    
    def get_absolute_url(self):
        return '/event/%s/' % str(self.id)
    
    def get_absolute_fburl(self):
        return '/fb%s' % self.get_absolute_url()
    

class Alert(Event):
    '''
        Alert son los recordatorios que el usuario crea solo
        para su uso propio y quiere que se le avise
    '''
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    date_starts = db.DateTimeProperty()
    date_ends = db.DateTimeProperty()
    poi = db.ReferenceProperty(POI, required=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, required=True, collection_name='alerts')
    done_when = db.DateTimeProperty()
    has = db.StringListProperty(default=[u'active:T', u'done:F', ])
    
    _done = False
    
    @classproperty
    def objects(self):
        return AlertHelper()
    
    def is_done(self):
        if 'done:T' in self.has:
            return True
        return False
    
    def toggle_done(self):
        if self.is_done():
            self.has.remove(u'done:T')
            self.has.append(u'done:F')
            return False
        self.has.remove(u'done:F')
        self.has.append(u'done:T')
        self._done = True
        self.done_when = datetime.now()  # set done time
        return True
    
    @classmethod
    def update_or_insert(cls, id = None, name = None, description = None,
                         date_starts = None, date_ends = None, poi = None,
                         user = None, done = False, active = None, done_when=None):
        '''
            Crea una alerta nueva, si recibe un id, la busca y actualiza.
            
            :returns: :class:`geoalert.models.Alert`
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`, :class:`TypeError`
        '''
        if not isinstance(user, User):
            raise AttributeError()
        if poi is None or not isinstance(poi, POI):
            raise AttributeError()
        if name is None or not isinstance(name, basestring):
            raise AttributeError()
        if description is not None and not isinstance(description, basestring):
            raise AttributeError()
        if id is not None:  # como se ha pasado un id, queremos modificar una alerta existente
            alert = cls.objects.get_by_id_user(id, user)
            if alert is None:
                return None
            alert.name = name
            alert.description = description
            alert.date_starts = date_starts
            alert.date_ends = date_ends
            alert.poi = poi
            if active is not None and alert.is_active() != active:
                alert.toggle_active()
            if alert.is_done() != done:
                alert.toggle_done()
            alert.put()
            return alert
        else:
            alert = Alert(name = name, description = description, date_starts = date_starts,
                          date_ends = date_ends, poi = poi, user = user)
            if done:
                alert.toggle_done()
                if done_when is not None:
                    alert.done_when = done_when
            if active == False:
                alert.toggle_active()
            
            alert.put()
            return alert
        
    def put(self, from_comment=False):
        if self.is_saved():
            super(Alert, self).put()
            if from_comment:
                return self 
            if self._done:
                alert_done.send(sender=self)
            else:
                alert_modified.send(sender=self)
        else:
            super(Alert, self).put()
            alert_new.send(sender=self)
            
    def delete(self):
        alert_deleted.send(sender=self)
        d = _Deleted_Alert(deleted_id=self.id, user=self.user)
        put = db.put_async([d])
        super(Alert, self).delete()
        put.get_result()
        
    def to_dict(self):
            return {'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'poi_id': self.poi.key().id(),
                    'x': self.poi.location.lat,
                    'y': self.poi.location.lon,
                    'address': unicode(self.poi.address),
                    'created': long(time.mktime(self.created.timetuple())) if self.created else 0,
                    'modified': long(time.mktime(self.modified.timetuple())) if self.modified else 0,
                    'starts': long(time.mktime(self.date_starts.timetuple())) if self.date_starts else 0,
                    'ends': long(time.mktime(self.date_ends.timetuple())) if self.date_ends else 0,
                    'done_when': long(time.mktime(self.done_when.timetuple())) if self.done_when else 0,
                    'done': self.is_done(),
                    'distance':self.get_distance(),
                    'active': self.is_active(),
                    }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())
    
    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return self.name


class Suggestion(Event, Visibility, Taggable):
    '''
        Recomendaciones de los usuarios que otros pueden
        convertir en Alert
    '''
    slug = db.StringProperty()
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    date_starts = db.DateTimeProperty()
    date_ends = db.DateTimeProperty()
    hour_starts = db.DateTimeProperty(default=None)
    hour_ends = db.DateTimeProperty(default=None)
    poi = db.ReferenceProperty(POI, required=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, collection_name='suggestions')
    has = db.StringListProperty(default=[u'active:T',])
    _short_url = db.TextProperty()
    
    _counters = None
    _relevance = None
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [[], 'name', 'description', 'poi']
    
    @property
    def short_url(self):
        from os import environ
        if environ['REMOTE_ADDR'] == '127.0.0.1':
            return 'http://%s%s' % (environ['HTTP_HOST'], self.get_absolute_url())
        if self._short_url is None:
            self._get_short_url()
            if self._short_url is not None:
                self.put()
            else:
                from os import environ
                return 'http://%s%s' % (environ['HTTP_HOST'], self.get_absolute_url())
        return self._short_url
    
    @property
    def counters(self):
        if self._counters is None:
            self._counters = SuggestionCounter.all().ancestor(self).get()
        return self._counters
    
    @classproperty
    def objects(self):
        return SuggestionHelper()
    
    @classmethod
    def update_or_insert(cls, id = None, name = None, description = None,
                         date_starts = None, date_ends = None, hour_starts = None,
                         hour_ends = None, poi = None, user = None, done = False, 
                         active = True, tags = None, vis = 'public', commit=True, 
                         to_facebook=False, to_twitter=False):
        '''
            Crea una sugerencia nueva, si recibe un id, la busca y actualiza.
            
            :returns: :class:`geoalert.models.Suggestion`
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`, :class:`TypeError`
        '''
        if not isinstance(user, User):
            raise TypeError()
        if id is not None:  
            # como se ha pasado un id, queremos modificar una alerta existente
            sugg = cls.objects.get_by_id_user(id, user, querier=user)
            if sugg is None:
                return None
            if name is not None and name != '':
                from datetime import timedelta
                if sugg.created+timedelta(hours=2) > datetime.now():
                    sugg.name = name
            #sugg.name = name if name is not None else sugg.name
            sugg.description = description
            sugg.date_starts = date_starts
            sugg.date_ends = date_ends 
            sugg.hour_ends = hour_ends 
            sugg.poi = poi if poi is not None else sugg.poi
            if vis != '':
                sugg._vis = vis
            if sugg.is_active() != active:
                sugg.toggle_active()
            if tags != '':
                sugg._tags_setter(tags, commit=commit)
            elif commit:
                sugg.put()
        else:
            if poi is None:
                raise TypeError()
            sugg = Suggestion(name = name, description = description, date_starts = date_starts,
                          date_ends = date_ends, hour_starts = hour_starts, hour_ends = hour_ends, 
                          poi = poi, user = user, _vis=vis)
            if not active:
                sugg.toggle_active()
            if tags != '':
                sugg._tags_setter(tags, commit=commit)
            if commit:
                sugg.put()
                if to_facebook:
                    from facebookApp.watchers import new_suggestion
                    new_suggestion(sugg)
                if to_twitter:
                    if sugg._is_public():
                        if sugg.short_url is None:
                            sugg._get_short_url()
                        msg = _("#grm %s") % sugg.short_url
                        from geoauth.clients.twitter import TwitterClient
                        try:
                            tw_client=TwitterClient(user=sugg.user)
                            tw_client.send_tweet(msg, sugg.poi.location)
                        except:                 
                            pass
        return sugg
        
    def add_follower(self, user):
        '''
        Crea una alerta a partir de una sugerencia
        
            :param user: Usuario que quiere apuntarse a una sugerencia
            :type user: :class:`geouser.models.User`
            
            :returns: :class:`geoalert.models.AlertSuggestion`    
        '''
        if self.user.key() == user.key():
            return False
        def _tx(sug_key, user_key):
            sug = db.get(sug_key)
            # indice con personas que siguen la sugerencia
            index = SuggestionFollowersIndex.all().ancestor(sug).filter('count <', 80).get()
            if index is None:
                index = SuggestionFollowersIndex(parent=sug)
            index.keys.append(user_key)
            index.count += 1
            index.put()
            return True
        index = db.GqlQuery('SELECT __key__ FROM SuggestionFollowersIndex WHERE ancestor IS :1 AND keys = :2', self.key(), user.key()).get()
        if index is not None: # ya es seguidor
            a = AlertSuggestion.objects.get_by_sugid_user(self.id, user)
            if a is None: # ¿por algun motivo no la tiene en la mochila?
                trans = True
            else:
                return True
        elif self._is_public():
            trans = db.run_in_transaction(_tx, sug_key = self.key(), user_key = user.key())
        else:
            if self.user_invited(user):
                trans = db.run_in_transaction(_tx, sug_key = self.key(), user_key = user.key())
                if trans:
                    self.user_invited(user, set_status=1)
            else:
                raise ForbiddenAccess()
        if trans:
            alert = AlertSuggestion.update_or_insert(suggestion = self, user = user)
            suggestion_following_new.send(sender=self, user=user)
            return True
        return None
        
    
    def del_follower(self, user):
        '''
        Borra un usuario de la lista
        
            :param user: Usuario que quiere borrarse a una sugerencia
            :type user: :class:`geouser.models.User`   
        '''
        def _tx(index_key, user_key):
            index = db.get_async(index_key)
            index = index.get_result()
            index.keys.remove(user_key)
            index.count -= 1
            db.put_async([index])
        index = db.GqlQuery('SELECT __key__ FROM SuggestionFollowersIndex WHERE ancestor IS :1 AND keys = :2', self.key(), user.key()).get()
        suggestion_following_deleted.send(sender=self, user=user)
        if index is not None:
            db.run_in_transaction(_tx, index, user.key())      
            return True
        return False
    
    def put(self, from_comment=False):
        self.name = self.name.strip()
        if from_comment:
            # no escribir timeline si es de un comentario
            super(Suggestion, self).put()
            return self
        from django.template.defaultfilters import slugify
        # buscar slug
        
        if self.is_saved():
            # estamos modificando sugerencia
            super(Suggestion, self).put()
            suggestion_modified.send(sender=self)
        else:
            # nueva sugerencia
            if self.slug is None:
                name = self.name.lower()[:32]
                self.slug = unicode(slugify('%s'% (name)))
                p = Suggestion.all().filter('slug =', self.slug).get()
                if p is not None:
                    i = 1
                    while p is not None:
                        slug = self.slug + '-%s' % i
                        p = Suggestion.all().filter('slug =', slug).get()
                    self.slug = self.slug + '-%s' % i
            super(Suggestion, self).put()
            counter = SuggestionCounter(parent=self)
            put = db.put_async(counter)
            self._get_short_url()
            put.get_result()
            suggestion_new.send(sender=self)
            
    def _get_short_url(self):
        from libs.vavag import VavagRequest
        from os import environ
        try:
            from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global
            client = VavagRequest(__web_settings.SHORTENER_ACCESS['user'], __web_settings.SHORTENER_ACCESS['key'])
            response =  client.set_pack('%s%s' % (environ['HTTP_HOST'], self.get_absolute_url()))
            self._short_url = response['results']['packUrl']
        except:
            self._short_url = None
            
    def delete(self):
        from geolist.models import List
        added = db.GqlQuery("SELECT __key__ FROM Event WHERE suggestion = :1", self.key()).get()
        added_list = db.GqlQuery("SELECT __key__ FROM List WHERE keys = :1", self.key()).get()
        if added is None and added_list is None:
            # nadie la añadió
            suggestion_deleted.send(sender=self, user=self.user)
            return super(Suggestion, self).delete()
        from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global
        generico = User.objects.get_by_username(__web_settings.GENERICO, keys_only=True)
        if generico == Suggestion.user.get_value_for_datastore(self):
            from geolist.models import ListSuggestion 
            # es del usuario georemindme, la borramos
            alerts = AlertSuggestion.all().filter('suggestion =', self.key()).run()
            lists = ListSuggestion.all().filter('keys =', self.key()).run()
            to_save = []
            for l in lists:
                l.keys.remove(self.key())
                to_save.append(l)
            p = db.put_async(to_save)
            for a in alerts:
                a.delete()
            suggestion_deleted.send(sender=self, user=generico)
            p.get_result()
            return super(Suggestion, self).delete()
        # otro usuario, se la asignamos a georemindme
        viejo = self.user
        self.user = generico
        self.put()
        self.user.counters.set_suggested()
        suggestion_deleted.send(sender=self, user=viejo)
    
    def has_follower(self, user):
        if not user.is_authenticated():
            return False
        if db.GqlQuery('SELECT __key__ FROM SuggestionFollowersIndex WHERE ancestor IS :1 AND keys = :2', self.key(), user.key()).get() is not None:
            return True
        return False   
    
        
    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'poi_id': self.poi.key().id(),
                'x': self.poi.location.lat,
                'y': self.poi.location.lon,
                'address': self.poi.address,
                'tags': self.tags,
                'created': long(time.mktime(self.created.timetuple())) if self.created else 0,
                'modified': long(time.mktime(self.modified.timetuple())) if self.modified else 0,
                'starts': long(time.mktime(self.date_starts.timetuple())) if self.date_starts else 0,
                'ends': long(time.mktime(self.date_ends.timetuple())) if self.date_ends else 0,
                'active': self.is_active(),
                }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())

    def get_absolute_url(self):
        return '/suggestion/%s/' % self.slug.encode('utf-8') if self.slug is not None and self.slug != '' else self.id
    
    def get_absolute_fburl(self):
        return '/fb%s' % self.get_absolute_url()
    
    def insert_ft(self):
        """
            Añade la sugerencia a la tabla en fusiontables
            
            En caso de fallo, se guarda el punto en _Do_later_ft,
            para intentar añadirlo luego
        """
        if self._is_public():
            from mapsServices.fusiontable import ftclient, sqlbuilder
            try:
                ftclient = ftclient.OAuthFTClient()
                from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global
                import unicodedata
                name = unicodedata.normalize('NFKD', self.name).encode('ascii','ignore')
                return ftclient.query(sqlbuilder.SQL().insert(__web_settings.FUSIONTABLES['TABLE_SUGGS'],
                                                        {'name': name,
                                                        'location': '%s,%s' % (self.poi.location.lat, self.poi.location.lon),
                                                        'sug_id': self.id,
                                                        'modified': self.modified.isoformat(),
                                                        'created': self.created.isoformat(),
                                                        'relevance': self._calc_relevance(),
                                                         }
                                                       )
                               )
            except:  # Si falla, se guarda para intentar añadir mas tarde
                raise
                from georemindme.models_utils import _Do_later_ft
                later = _Do_later_ft(instance_key=self.key())
                later.put()
    
    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return self.name
    
    def _calc_relevance(self):
        if self._relevance is None:
            from geovote.models import Vote
            votes = Vote.objects.get_vote_counter(self.key())
            from datetime import datetime
            time = datetime.now() - self.modified
            self._relevance = (self.counters.followers*8 + votes*2) * 15/(time.days+1)
        return self._relevance
        

class AlertSuggestion(Event):
    '''
        Una recomendacion puede ser convertida en una Alerta, 
        para que se le avise al usuario
    '''
    suggestion = db.ReferenceProperty(Suggestion, required = True)
    done_when = db.DateTimeProperty()
    modified = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)
    user = db.ReferenceProperty(User, required=True, collection_name='alertsuggestions')
    has = db.StringListProperty(default=[u'active:T', u'done:F', ])
    
    _done = False
    @classproperty
    def objects(self):
        return AlertSuggestionHelper()
    
    def is_done(self):
        if 'done:T' in self.has:
            return True
        return False
    
    def toggle_done(self):
        if self.is_done():
            self.has.remove(u'done:T')
            self.has.append(u'done:F')
            return False
        self.has.remove(u'done:F')
        self.has.append(u'done:T')
        self._done = True
        self.done_when = datetime.now()  # set done time
        return True
    
    @classmethod
    def update_or_insert(cls, id = None, suggestion = None,
                         user = None, done = False, active = True):
        '''
            Crea una alerta de sugerencia nueva, si recibe un id, la busca y actualiza.
            
            :returns: :class:`geoalert.models.AlertSuggestion`
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`, :class:`TypeError`
        '''
        if not isinstance(user, User):
            raise TypeError()
        if suggestion is None:
            raise TypeError()
        if suggestion._is_private():
            if suggestion.user != user:
                raise ForbiddenAccess()
        if suggestion._is_shared():
            if not suggestion.user_invited(user):
                raise ForbiddenAccess()
        if id is not None:  # como se ha pasado un id, queremos modificar una alerta existente
            alert = cls.objects.get_by_id_user(id, user)
            if alert is None:
                return None
            if alert.is_active() != active:
                alert.toggle_active()
            if alert.is_done() != done:
                alert.toggle_done()
            alert.put()
            return alert
        else:
            alert = AlertSuggestion(suggestion = suggestion, user = user)
            if done:
                alert.toggle_done()
            if not active:
                alert.toggle_active()
            alert.put()
            return alert
        
    def put(self, from_comment=False):
        if self.is_saved():
            super(AlertSuggestion, self).put()
            if from_comment:
                return self
            if self._done:
                alert_done.send(sender=self)
            else:
                alert_modified.send(sender=self)
        else:
            super(AlertSuggestion, self).put()
            alert_new.send(sender=self)
        
    def to_dict(self):
            return {'id': self.id,
                    'name': self.suggestion.name,
                    'description': self.suggestion.description,
                    'poi_id': self.suggestion.poi.id,
                    'x': self.suggestion.poi.location.lat,
                    'y': self.suggestion.poi.location.lon,
                    'address': unicode(self.suggestion.poi.address),
                    'created': long(time.mktime(self.created.timetuple())) if self.suggestion.created else 0,
                    'modified': long(time.mktime(self.modified.timetuple())) if self.suggestion.modified else 0,
                    'starts': long(time.mktime(self.suggestion.date_starts.timetuple())) if self.suggestion.date_starts else 0,
                    'ends': long(time.mktime(self.suggestion.date_ends.timetuple())) if self.suggestion.date_ends else 0,
                    'done_when': long(time.mktime(self.suggestion.done_when.timetuple())) if self.suggestion.done_when else 0,
                    'done': self.is_done(),
                    'active': self.is_active(),
                    }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())
        
    def __str__(self):
        return unicode(self.suggestion.name).encode('utf-8')

    def __unicode__(self):
        return self.suggestion.name


class _Deleted_AlertHelper(object):
    def get_by_id_user(self, id, user):
        '''
        Obtiene el evento con ese id comprobando que
        pertenece al usuario
        
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`
        '''
        if not isinstance(user, User):
            raise TypeError()
        event = _Deleted_Alert.get_by_id(int(id))
        if event.user.key() == user.key():
            return event
        return None
    
    def get_by_last_sync(self, user, last_sync):
        '''
        Obtiene los ultimos eventos a partir
        de una fecha de ultima sincronizacion
        '''
        if not isinstance(user, User):
            raise TypeError()
        return _Deleted_Alert.all().filter('user =', user).filter('created >', last_sync).order('-created')


class _Deleted_Alert(db.Model):
    deleted_id = db.IntegerProperty()
    user = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
    objects = _Deleted_AlertHelper()
    
    @property
    def id(self):
        return int(self.deleted_id)


from helpers import *
