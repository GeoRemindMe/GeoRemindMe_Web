# coding=utf-8

"""
.. module:: models_social
    :platform: appengine
    :synopsis: Modelos con los datos de las redes sociales
"""


from django.utils.translation import gettext_lazy as _

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from models import User
from georemindme import model_plus


class SocialUser(polymodel.PolyModel, model_plus.Model):    
    uid = db.StringProperty(required=False)
    email = db.EmailProperty(required=False)
    realname = db.TextProperty(indexed=False)
    created = db.DateTimeProperty(auto_now_add=True)
    user = None
    
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
        ugoogle = GoogleUser.get_by_key_name('gu%s' % uid)
        return ugoogle
    
    
class GoogleUser(SocialUser):
    """USERS FROM A GOOGLE ACCOUNT"""
    user = db.ReferenceProperty(User)
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
        from signals import user_social_new
        user_social_new.send(sender=ugoogle)
        return ugoogle    
    
    def update(self, email, realname):
        self.realname= realname
        self.email = email
        self.put()
        
    def has_perms(self, uid):
        from geoauth.models import OAUTH_Access
        if OAUTH_Access.get_token_user('google', self.user) is None:
            return False
        return True

    
class FacebookUserHelper():
    def get_by_id(self, uid):
        """Search and returns a User object with that email"""
        if uid is None:
            raise db.BadValueError("Wrong id")
        ufacebook = FacebookUser.get_by_key_name('fu%s' % uid)
        return ufacebook


class FacebookUser(SocialUser):
    """USERS FROM FACEBOOK"""
    user = db.ReferenceProperty(User)
    profile_url = db.URLProperty(indexed=False)
    access_token = db.TextProperty()
    objects = FacebookUserHelper()
    
    def is_facebook(self):
        return True

    def has_perms(self):
        from geoauth.models import OAUTH_Access
        if OAUTH_Access.get_token_user('facebook', self.user) is None:
            return False
        return True
        
    @classmethod
    def register(cls, user, uid, email, realname, profile_url, access_token):
        def _tx():
            key_name = 'fu%s' % uid
            ufacebook = FacebookUser(key_name=key_name, user=user, 
                                   uid=str(uid), email=email, 
                                   realname=realname, profile_url=profile_url, 
                                   access_token=access_token)
            ufacebook.put()
            return ufacebook
        ufacebook = db.run_in_transaction(_tx)
        from signals import user_social_new
        user_social_new.send(sender=ufacebook)
        return ufacebook
    
    def update(self, realname, profile_url, uid=None):
        if uid is not None:
            self.uid = uid
        self.realname= realname
        self.profile_url = profile_url
        self.put()


class TwitterUserHelper():
    def get_by_id(self, uid):
        """Search and returns a User object with that email"""
        if uid is None:
            raise db.BadValueError("Wrong id")
        utwitter = TwitterUser.get_by_key_name('tu%s' % uid)
        return utwitter


class TwitterUser(SocialUser):
    """USER FROM TWITTER"""
    user = db.ReferenceProperty(User)
    username = db.TextProperty()
    picurl = db.URLProperty(indexed=False)
    objects = TwitterUserHelper()
    
    def is_twitter(self):
        return True
    
    def has_perms(self, uid):
        from geoauth.models import OAUTH_Access
        if OAUTH_Access.get_token_user('twitter', self.user) is None:
            return False
        return True
        
    @classmethod
    def register(cls, user, uid, username, realname, picurl):
        def _tx():
            key_name = 'tu%s' % uid
            utwitter = TwitterUser(key_name=key_name, user=user, uid=str(uid), username=username, realname=realname, picurl=picurl)
            utwitter.put()
            return utwitter
        utwitter = db.run_in_transaction(_tx)
        from signals import user_social_new
        user_social_new.send(sender=utwitter)
        return utwitter         
    
    def update(self, username, realname, picurl):
        self.username = username
        self.realname= realname
        self.picurl = picurl
        self.put()