# coding=utf-8

from datetime import datetime
import time

from django.utils.translation import ugettext as _
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
        return self.key().id()

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
        return '/event/%s' % str(self.id)
    

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
        return unicode(self.name)
    
    def __unicode__(self):
        return self.name


class Suggestion(Event, Visibility, Taggable):
    '''
        Recomendaciones de los usuarios que otros pueden
        convertir en Alert
    '''
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    date_starts = db.DateTimeProperty()
    date_ends = db.DateTimeProperty()
    poi = db.ReferenceProperty(POI, required=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, required=True, collection_name='suggestions')
    has = db.StringListProperty(default=[u'active:T',])
    
    _counters = None
    
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
                         date_starts = None, date_ends = None, poi = None,
                         user = None, done = False, active = True, vis = 'public'):
        '''
            Crea una sugerencia nueva, si recibe un id, la busca y actualiza.
            
            :returns: :class:`geoalert.models.Suggestion`
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`, :class:`TypeError`
        '''
        if not isinstance(user, User):
            raise TypeError()
        if poi is None:
            raise TypeError()
        if id is not None:  # como se ha pasado un id, queremos modificar una alerta existente
            sugg = cls.objects.get_by_id_user(id, user)
            if sugg is None:
                return None
            sugg.name = name if name is not None else sugg.name
            sugg.description = description if description is not None else sugg.description
            sugg.date_starts = date_starts if date_starts is not None else sugg.date_starts
            sugg.date_ends = date_ends if date_ends is not None else sugg.date_ends
            sugg.poi = poi if poi is not None else sugg.poi
            sugg._vis = vis
            if sugg.is_active() != active:
                sugg.toggle_active()
            sugg.put()
            return sugg
        else:
            sugg = Suggestion(name = name, description = description, date_starts = date_starts,
                          date_ends = date_ends, poi = poi, user = user, _vis=vis)
            if not active:
                sugg.toggle_active()
            sugg.put()
            counter = SuggestionCounter(parent=sugg)
            counter.put()
            return sugg
        
    def add_follower(self, user):
        '''
        Crea una alerta a partir de una sugerencia
        
            :param user: Usuario que quiere apuntarse a una sugerencia
            :type user: :class:`geouser.models.User`
            
            :returns: :class:`geoalert.models.AlertSuggestion`    
        '''
        def _tx(sug_key, user_key):
            # TODO : cambiar a contador con sharding
            sug = db.get(sug_key)
            # indice con personas que siguen la sugerencia
            index = SuggestionFollowersIndex.all().ancestor(sug).filter('count <', 80).get()
            if index is None:
                index = SuggestionFollowersIndex(parent=sug)
            index.keys.append(user_key)
            index.count += 1
            db.put_async([sug, index])
        if SuggestionFollowersIndex.all().ancestor(self).filter('keys =', user.key()).count() != 0:
            a = AlertSuggestion.objects.get_by_sugid_user(self.id, user)
            if a is None:
                return True
            else:
                return a
        if self._is_public():
            trans = db.run_in_transaction(_tx, sug_key = self.key(), user_key = user.key())
        else:
            if self.user_invited(user):
                trans = db.run_in_transaction(_tx, sug_key = self.key(), user_key = user.key())
            else:
                raise ForbiddenAccess()
        self.user_invited(user, set_status=1) 
        self.counters.set_followers(+1)  # incrementar contadores
        alert = AlertSuggestion.update_or_insert(suggestion = self, user = user)
        suggestion_following_new.send(sender=self, user=user)

        return alert
    
    def del_follower(self, user):
        '''
        Borra un usuario de la lista
        
            :param user: Usuario que quiere borrarse a una sugerencia
            :type user: :class:`geouser.models.User`   
        '''
        def _tx(sug_key, index_key, user_key):
            sug = db.get_async(sug_key)
            index = db.get_async(index_key)
            sug = sug.get_result()
            index = index.get_result()
            index.keys.remove(user_key)
            index.count -= 1
            db.put_async([index, sug])
        index = SuggestionFollowersIndex.all().ancestor(self.key()).filter('keys =', user.key()).get()
        if index is not None:
            db.run_in_transaction(_tx, self.key(), index.key(), user.key())
            self.counters.set_followers(-1)
            suggestion_following_deleted.send(sender=self, user=user)
            return True
        return False
    
    def put(self, from_comment=False):
        if self.is_saved():
            super(Suggestion, self).put()
            if from_comment:
                return self
            suggestion_modified.send(sender=self)
        else:
            super(Suggestion, self).put()
            suggestion_new.send(sender=self)
            
    def delete(self):
        children = db.query_descendants(self).fetch(10)
        for c in children:
            c.delete()
        suggestion_deleted.send(sender=self)
        super(Suggestion, self).delete()
    
    def user_invited(self, user, set_status=None):
        '''
        Comprueba que un usuario ha sido invitado a la lista
            
            :param user: Usuario que debe estar invitado
            :type user: :class:`geouser.models.User`
            :param set_status: Nuevo estado para la invitacion
            :type set_status: :class:`integer`
            
            :returns: True si esta invitado, False en caso contrario
        '''
        from georemindme.models_indexes import Invitation
        if set_status is None:
            invitation = Invitation.objects.is_user_invited(self, user)
            return invitation
        else:
            invitation = Invitation.objects.get_invitation(self, user)
            if invitation is not None:
                invitation.set_status(set_status)
        return invitation
    
    def has_follower(self, user):
        if SuggestionFollowersIndex.all().ancestor(self.key()).filter('keys =', user.key()).count() != 0:
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
                'created': long(time.mktime(self.created.timetuple())) if self.created else 0,
                'modified': long(time.mktime(self.modified.timetuple())) if self.modified else 0,
                'starts': long(time.mktime(self.date_starts.timetuple())) if self.date_starts else 0,
                'ends': long(time.mktime(self.date_ends.timetuple())) if self.date_ends else 0,
                'active': self.is_active(),
                }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())
    
    def __str__(self):
        return unicode(self.name)
    
    def __unicode__(self):
        return self.name
    
    def send_invitation(self, sender, to):
        if sender.key() == self.user.key():
            from georemindme.models_indexes import Invitation
            invitation = Invitation.send_invitation(sender=sender, to=to, instance=self)
            if invitation is not None:
                return True
            return False
        else:
            raise ForbiddenAccess
        
        

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
            
    def delete(self):
        alert_deleted.send(sender=self)
        super(Alert, self).delete()
        
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
        return self.deleted_id

from watchers import *    
from helpers import *
