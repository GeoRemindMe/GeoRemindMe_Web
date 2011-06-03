from datetime import datetime
from time import time
import os
from random import randrange

from google.appengine.ext import db
from google.appengine.ext.db import BadValueError, Key

from django.conf import settings
from django.utils.hashcompat import md5_constructor

from geouser.models import User

from memcache import *

MAX_SESSION_KEY = 18446744073709551616L

class UserRPCHelper(object):
    """
        Do the queries needed to get a object
        Use ->  User.object.method()
    """
    def get_by_id(self, session_id):
        '''
            Return the userRPC from the session_id
            if session expired, returns None
        '''
        userRPC = deserialize_instances(memcache.get("%sUSERRPC" % session_id))
        if not userRPC:
            userRPC = self._get().filter('session_id =', session_id).get()
            
            if userRPC is None:
                return None
            
            if userRPC.is_valid(): 
                memcache.set("%sUSERRPC" % session_id, serialize_instances(userRPC))
                return userRPC
        
        if userRPC.is_valid():
            return userRPC
            
        return None
        
    def get_by_email(self, email):
        """
         Search and returns a User object with that email
        """
        if email is None:
            raise BadValueError("Wrong email")
        userRPC = self._get().filter('email =', email).get()
        if userRPC:
            if userRPC.is_valid():
                return userRPC
            else:
                userRPC.delete()
        return None
    
    def get_by_key(self,key):
        user = UserRPC.get(Key(encoded=key))
        if user.is_valid():
            return user
        return None
        
    
    def _get(self, string=None):
        return UserRPC.all()

class UserRPC(db.Model):
    email = db.EmailProperty(required=True)
    session_id = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True, indexed=False)
    expire_date = db.DateTimeProperty(indexed=False)
    realuser = db.ReferenceProperty(User)
    objects = UserRPCHelper()
    
    def put(self):
        t = time() + settings.SESSION_COOKIE_AGE
        self.expire_date = datetime.fromtimestamp(t)
        if self.session_id is None:
            self.session_id= self._new_session_id()
            
        memcache.delete("%sUSERRPC" % self.session_id)
        super(self.__class__, self).put()
        
    def is_valid(self):
        if self.expire_date > datetime.now():
            return True
        else:
            return False
        
    def _new_session_id(self):
        """
            Creates a new user id
        """
        try:
            pid = os.getpid()
        except AttributeError:
            pid = 1
        while 1:
            session_id = md5_constructor("%s%s%s%s"
                                      % (randrange(0, MAX_SESSION_KEY), pid, time(),
                                        settings.SECRET_KEY)).hexdigest()
            if not self._exists_session_id(session_id):
                return session_id
    
    def _exists_session_id(self, session_id):
        """
            Check if user_id exists
        """
        if UserRPC.all().filter("session_id = ", session_id).get() is not None:
            return True
        else:
            return False
