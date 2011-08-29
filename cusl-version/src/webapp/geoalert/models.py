# coding=utf-8

from datetime import datetime

from django.utils.translation import ugettext as _
from django.utils import simplejson
from google.appengine.ext import db, search
from google.appengine.ext.db import polymodel
from google.appengine.ext.db import BadValueError

from models_poi import *
from georemindme.models_utils import Visibility
from georemindme.decorators import classproperty
from exceptions import ForbiddenAccess
from geouser.models import User
from geotags.models import Taggable
from geouser.models_acc import UserTimelineSystem


class Event(polymodel.PolyModel, search.SearchableModel, Taggable):
    """Informacion comun para las alertas y recomendaciones"""
    name = db.StringProperty(required=True)
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    date_starts = db.DateTimeProperty()
    date_ends = db.DateTimeProperty()
    poi = db.ReferenceProperty(POI, required=True)
    user = db.ReferenceProperty(User, required=True, collection_name='alerts')
    modified = db.DateTimeProperty(auto_now=True)
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

    def put(self):
        try:
            if self.date_ends < self.date_starts:
                raise BadValueError()
        except TypeError:
            pass        
        super(polymodel.PolyModel, self).put()

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
        return '/event/view/%s' % str(self.key().id())
    

class Alert(Event):
    '''
        Alert son los recordatorios que el usuario crea solo
        para su uso propio y quiere que se le avise
    '''
    done_when = db.DateTimeProperty()
    has = db.StringListProperty(default=[u'active:T', u'done:F', ])
    
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
        self.done_when = datetime.now()  # set done time
        return True
    
    @classmethod
    def update_or_insert(cls, id = None, name = None, description = None,
                         date_starts = None, date_ends = None, poi = None,
                         user = None, done = False, active = True):
        '''
            Crea una alerta nueva, si recibe un id, la busca y actualiza.
            
            :returns: :class:`geoalert.models.Alert`
            :raises: :class:`geoalert.exceptions.ForbiddenAccess`, :class:`TypeError`
        '''
        if not isinstance(user, User):
            raise TypeError()
        if poi is None:
            raise TypeError()
        if id is not None:  # como se ha pasado un id, queremos modificar una alerta existente
            alert = cls.objects.get_by_id_user(id, user)
            if alert is None:
                return None
            alert.name = name
            alert.description = description
            alert.date_starts = date_starts
            alert.date_ends = date_ends
            alert.poi = poi
            if alert.is_active() != active:
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
            if not active:
                alert.toggle_active()
            alert.put()
            timeline = UserTimelineSystem(user = user, instance = alert, msg_id=200)
            timeline.put()
            return alert
        
    def to_dict(self):
            return {'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'poi_id': self.poi.key().id(),
                    'x': self.poi.point.lat,
                    'y': self.poi.point.lon,
                    'address': unicode(self.poi.address),
                    'starts': unicode(self.date_starts.strftime("%d%b")) if self.date_starts else '',
                    'ends': unicode(self.date_ends.strftime("%d%b")) if self.date_ends else '',
                    'donedate': unicode(self.done_when.strftime("%d%b")) if self.done_when else '',
                    'done': self.is_done(),
                    'distance':self.get_distance() 
                    }
            
    def to_json(self):
        return simplejson.dumps(self.to_dict())
    
    def __str__(self):
        return self.name


class Suggestion(Event, Visibility):
    '''
        Recomendaciones de los usuarios que otros pueden
        convertir en Alert
    '''
    pass

class AlertSuggestion(Taggable):
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
        self.done_when = datetime.now()  # set done time
        return True
    
    @classmethod
    def update_or_insert(cls, id = None, suggestion = None,
                         user = None, done = False, active = True):
        if not isinstance(user, User):
            raise TypeError()
        if suggestion is None:
            raise TypeError()
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
            timeline = UserTimelineSystem(user = user, instance = alert, msg_id=200)
            timeline.put()
            return alert
        
    def __str__(self):
        return self.suggestion.name
            
    
from helpers import *