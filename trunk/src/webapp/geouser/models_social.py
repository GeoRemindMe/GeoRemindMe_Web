# coding=utf-8

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from models import User


class SocialUser(polymodel.PolyModel):
    user = db.ReferenceProperty(User)
    uid = db.StringProperty(required=False)
    email = db.EmailProperty(required=False)
    realname = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    def is_google(self):
        return False
    
    def is_facebook(self):
        return False
    
    def is_twitter(self):
        return False
    
    def set_user(self, user):
        def _tx():
            self.user = user
            self.put()
        db.run_in_transaction(_tx)

    
class GoogleUserHelper():
    def get_by_id(self, uid):
        """Search and returns a User object with that email"""
        if uid is None:
            raise db.BadValueError("Wrong id")
        #ugoogle = GoogleUser.all().filter('uid =', uid).get()
        ugoogle = GoogleUser.get_by_key_name('gu%s' % uid)
        return ugoogle
    
class GoogleUser(SocialUser):
    """USERS FROM A GOOGLE ACCOUNT"""
    objects = GoogleUserHelper()
    
    def is_google(self):
        return True
           
    @classmethod
    def register(cls, user, uid, email, realname):
        def _tx():
            key_name = 'gu%s' % uid
            ugoogle = GoogleUser(key_name=key_name, user=user, uid=str(uid), email=email, realname=realname)
            ugoogle.put()
            return ugoogle
        ugoogle = db.run_in_transaction(_tx)
        return ugoogle    
    
    def update(self, email, realname):
        self.realname= realname
        self.email = email
        self.put()

    
class FacebookUser(SocialUser):
    """USERS FROM FACEBOOK"""
    
    def is_facebook(self):
        return True


class TwitterUserHelper():
    
    def get_by_id(self, uid):
        """Search and returns a User object with that email"""
        if uid is None:
            raise db.BadValueError("Wrong id")
        utwitter = TwitterUser.get_by_key_name('tu%s' % uid)
        return utwitter

        
class TwitterUser(SocialUser):
    """USER FROM TWITTER"""
    username = db.TextProperty()
    picurl = db.URLProperty()
    objects = TwitterUserHelper()
    
    def is_twitter(self):
        return True
        
    @classmethod
    def register(cls, user, uid, username, realname, picurl):
        def _tx():
            key_name = 'tu%s' % uid
            utwitter = TwitterUser(key_name=key_name, user=user, uid=str(uid), username=username, realname=realname, picurl=picurl)
            utwitter.put()
            return utwitter
        utwitter = db.run_in_transaction(_tx)
        return utwitter         
    
    def update(self, username, realname, picurl):
        self.username = username
        self.realname= realname
        self.picurl = picurl
        self.put()