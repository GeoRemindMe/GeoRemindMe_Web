# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.


"""
from django.conf import settings

from django.utils.translation import ugettext as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel, Key, BadValueError
from memcache import *
from properties import PasswordProperty
from models_utils import Counter

class UserHelper(object):
    """
        Do the queries needed to get a object
        Use ->  User.object.method()
    """
    def get_by_key(self, key):
        return User.get(Key(encoded=key))
    
    def get_by_google_id(self, id):
        """
         Search and returns a User object with that email
        """
        
        if id is None:
            raise BadValueError("Wrong id")
        
        user = self._get().filter('google_id =', id).get()
        return user
    
    def get_by_email(self, email):
        """
         Search and returns a User object with that email
        """
        
        if email is None:
            raise BadValueError("Wrong email")
        
        user = deserialize_instances(memcache.get(email))
        if not user:
            #user = self._get().filter('email =', email).filter('has =', 'confirmed:T').get()
            user = self._get().filter('email =', email).get()
            memcache.set('%s%s' % (version, email), serialize_instances(user))
        return user
    
    def get_by_email_not_confirm(self, email):
        """
         Search and returns a User object with that email
         Search users with confirm True or False
        """
        if email is None:
            raise BadValueError("Wrong email")
        
        user = self._get().filter('email =', email).filter('has =', 'confirmed:F').get()
        return user
    
    def _get(self, string=None):
        return User.all().filter('has =', 'active:T')
class User(polymodel.PolyModel):
    created = db.DateTimeProperty(auto_now_add=True)
    last_point = db.GeoPtProperty(required=True, default=db.GeoPt(37.176487, -3.597929))
    has = db.StringListProperty(default=['active:T', 'confirmed:F', 'admin:F'])
    last_login = db.DateTimeProperty(indexed=False)
    from appengine_utilities.sessions import _AppEngineUtilities_Session 
    _session = db.ReferenceProperty(_AppEngineUtilities_Session)  
    objects = UserHelper()

    @property
    def profile(self):
        return self.profiles.get()
    
    def is_google_account(self):
        return False
    
    def is_geouser(self):
        return False
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        if 'active:T' in self.has:
            return True
        return False
    
    def is_confirmed(self):
        if 'confirmed:T' in self.has:
            return True
        return False
    
    def is_admin(self):
        if 'admin:T' in self.has:
            return True
        return False
    
    def toggle_active(self):
        if self.is_active():
            self.has.remove('active:T')
            self.has.append('active:F')
            return False
        self.has.remove('active:F')
        self.has.append('active:T')
        return True
    
    def toggle_confirmed(self):
        if self.is_confirmed():
            self.has.remove('confirmed:T')
            self.has.append('confirmed:F')
            return False
        self.has.remove('confirmed:F')
        self.has.append('confirmed:T')
        return True
    
    def toggle_admin(self):
        if self.is_admin():
            self.has.remove('admin:T')
            self.has.append('admin:F')
            return False
        self.has.remove('admin:F')
        self.has.append('admin:T')
        return True
        
    @classmethod
    def make_random_password(self, length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        #"Generates a random password with the given length and given allowed_chars"
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        
        # I take this from django.contrib.auth
        from random import choice
        return ''.join([choice(allowed_chars) for i in range(length)])
class GeoUser(User):
    email = db.EmailProperty(required=True)
    password = PasswordProperty(required=True, indexed=False)
    confirm_code = db.TextProperty(indexed=False)
    
    def put(self):
        # Ensure that email is unique
        u = GeoUser.all().filter('email =', self.email).get()
        if u is not None and u.key() != self.key():
            raise self.UniqueEmailConstraint(self.email)
        memcache.delete('%s%s' % (version, self.email))
        super(self.__class__, self).put()
    
    def check_password(self, raw):
        """
            Check password, raw is the password in plain text
        """
        alg, seed, passw = self.password.split('$')
        from django.utils.hashcompat import sha_constructor
        return passw == sha_constructor(seed + raw).hexdigest()
    
    def send_confirm_code(self):
        if not self.is_confirmed():
            self.confirm_code = self.make_random_password(length=24)#generate random number
            self.put()
        from mails import send_confirm_mail
        send_confirm_mail(self.email, self.confirm_code)#send mail
        
    def is_geouser(self):
        return True
    
    class UniqueEmailConstraint(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return _('User already in use: %S') % self.value
class GoogleUser(User):
    google_id = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    
    def put(self):
        # Ensure that email is unique
        memcache.delete('%s%s' % (version, self.email))
        super(self.__class__, self).put()
    
    def is_google_account(self):
        return True
class UserProfile(db.Model):
    user = db.ReferenceProperty(User, collection_name='profiles', required=True)
    remind_code = db.TextProperty(indexed=False)
    date_remind = db.DateTimeProperty(indexed=False)
    
    def send_remind_code(self):
        self.remind_code = self.user.make_random_password(length=24)
        from datetime import datetime
        self.date_remind = datetime.now()
        self.put()
        from mails import send_remind_pass_mail
        send_remind_pass_mail(self.user.email, self.remind_code)#send mail
    
        
# Means Point Of Interest (it is extended by Point)
class POI(polymodel.PolyModel):
    name = db.StringProperty(required=True)
    bookmark = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
class Point(POI):
    address = db.StringProperty()
    business = db.StringProperty()
    google_places_id = db.StringProperty(default=None) 
    point = db.GeoPtProperty() #GeoPtProperty? -> http://code.google.com/intl/es/appengine/docs/python/datastore/typesandpropertyclasses.html#GeoPtProperty
    geoboxes = db.StringListProperty()
    
    def put(self):
        from geobox import generate_geoboxes
        self.geoboxes = generate_geoboxes(self.point.lat, self.point.lon)
        
        super(self.__class__, self).put()
    
# Like pharmacy, library, .. .
class Business(POI):
    business = db.StringProperty()
class AlertHelper(object):
    
    def get_by_user(self, user, page=None, offset=0, limit=settings.MAX_ALERTS_PER_PAGE): # accepts user as email or instance
        if page:
            offset = (page - 1) * limit
            
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            alerts = deserialize_instances(memcache.get('%s%sALERT' % (version, user.key())))
            if not alerts:#save alerts in memcache
                alerts = self._get(user).fetch(limit=1000)
                if len(alerts) == 1000:
                    i = 1
                    while len(alerts) == 1000 * i:
                        alerts.append(self._get(user).fetch(offset=1000 * i, limit=1000))
                        i += 1
                memcache.set('%s%sALERT' % (version, user.key()), serialize_instances(alerts))
            
            return alerts[offset:offset + limit]
        
        return None
            
    def get_by_user_done(self, user, page=None, offset=0, limit=settings.MAX_ALERTS_PER_PAGE):
        if page:
            offset = (page - 1) * limit
            
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            alerts = deserialize_instances(memcache.get('%s%sALERTdone' % (version, user.key())))
            if not alerts:#save alerts in memcache
                alerts = self._get(user).filter('has =', 'done:T').fetch(limit=1000)
                if len(alerts) == 1000:
                    i = 1
                    while len(alerts) == 1000 * i:
                        alerts.append(self._get(user).filter('has =', 'done:T').fetch(offset=1000 * i, limit=1000))
                        i += 1
                memcache.set('%s%sALERTdone' % (version, user.key()), serialize_instances(alerts))
            return alerts[offset:offset + limit]
        
        return None
        
    def get_by_user_undone(self, user, page=None, offset=0, limit=settings.MAX_ALERTS_PER_PAGE):
        if page:
            offset = (page - 1) * limit
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            alerts = deserialize_instances(memcache.get('%s%sALERTundone' % (version, user.key())))
            if not alerts:#save alerts in memcache
                alerts = self._get(user).filter('has =', 'done:F').fetch(limit=1000)
                if len(alerts) == 1000:
                    i = 1
                    while len(alerts) == 1000 * i:
                        alerts.append(self._get(user).filter('has =', 'done:F').fetch(offset=1000 * i, limit=1000))
                        i += 1
                memcache.set('%s%sALERTundone' % (version, user.key()), serialize_instances(alerts))
            return alerts[offset:offset + limit]
        
        return None
    
    def get_by_key(self, key):
        return Alert.get(Key(encoded=key))
    
    def get_by_key_user(self, key, user):
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            return self._get(user).filter("key =", key).get()
        return None
    
    def get_by_id_user(self, id, user):
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            return self._get(user).filter('id =', id).get()
        return None
    
    def get_by_last_sync(self, user, last_sync):
        if type(user) == str or type(user) == db.Email:
            user = User.objects.get_by_email(user)
        if user:
            alerts = self._get(user).filter('modified >=', last_sync).fetch(limit=1000)
            if len(alerts) == 1000:
                i = 1
                while len(alerts) == 1000 * i:
                    alerts.append(self._get(user).filter('modified >=', last_sync).fetch(offset=1000 * i, limit=1000))
                    i += 1
            return alerts
        return None

    def _get(self, user):
        return user.alerts.order("-modified")

# When you add a reminder, an Alert is added
class Alert(db.Model):
    id = db.IntegerProperty(indexed=True)
    name = db.StringProperty(required=True)
    starts = db.DateTimeProperty()
    ends = db.DateTimeProperty()
    description = db.TextProperty()
    attachment = db.LinkProperty(indexed=False)#URL to file
    poi = db.ReferenceProperty(POI, required=True)
    user = db.ReferenceProperty(User, required=True, collection_name='alerts')
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    done_when = db.DateTimeProperty()
    #in the appengine datastore, is more eficient to use stringlistproperty than some booleanProperty, its only needs one index
    #I now alert only have 2 boolean by now, but is better to learn these things.  
    #see tip #6 and #7 -> http://googleappengine.blogspot.com/2009/06/10-things-you-probably-didnt-know-about.html
    has = db.StringListProperty(default=[u'active:T', u'done:F', ])
    order = db.IntegerProperty()
    objects = AlertHelper()   

    def put(self):
        try:
            if self.ends < self.starts:
                raise BadValueError()
        except TypeError:
            pass        
        if not self.id:#incrementa la id
            self.id = Counter.get_counter(str(self.__class__))
        memcache.delete('%s%sALERT' % (version, self.user.key()))
        super(self.__class__, self).put()

    def delete(self):
        try:
            if self.ends < self.starts:
                raise BadValueError()
        except TypeError:
            pass        
        memcache.delete('%s%sALERT' % (version, self.user.key()))
        super(self.__class__, self).delete()
    
    def is_active(self):
        if 'active:T' in self.has:
            return True
        return False
    
    def is_done(self):
        if 'done:T' in self.has:
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
        
    def toggle_done(self):
        memcache.delete('%s%sALERTdone' % (version, self.user.key()))
        memcache.delete('%s%sALERTundone' % (version, self.user.key()))
        if self.is_done():
            self.has.remove(u'done:T')
            self.has.append(u'done:F')
            return False
        self.has.remove(u'done:F')
        self.has.append(u'done:T')
        from datetime import datetime
        self.done_when = datetime.now()#set done time
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
        return '/user/view/%s' % str(self.id)
