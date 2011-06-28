# coding=utf-8
"""
.. module:: OAUTH_Models
    :platform: appengine
    :synopsis: OAUTH Models
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""

from uuid import uuid4
from time import time
import base64

from google.appengine.ext import db

from geouser.models import User
from exceptions import OAUTHException

class OAUTH_Client(db.Model):
    """Applications using our data"""
    # oauth_key is the Model's key_name field
    client_secret = db.TextProperty()
    client_verifier = db.TextProperty()
    user = db.ReferenceProperty(User)
    name = db.TextProperty()
    description = db.TextProperty()
    image = db.IMProperty()
    callback = db.URLProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def generate(cls, *args, **kwargs):
        def _generate_key():
            #genera una cadena de numeros aleatoria, se codifica a base64 y se limpia para URLs
            u = uuid4()
            return base64.urlsafe_b64encode(u.bytes.encode("base64")).strip('=')
        kwargs['key_name'] = 'oclient_%s' % _generate_key()
        kwargs['client_secret'] = _generate_key()
        client = OAUTH_Client(*args, **kwargs)
        client.put()
        return client
    
    @classmethod
    def get_token(cls, key_name):
        return OAUTH_Client.get_by_key_name('oclient_%s' % key_name)  
    
    @property
    def client_key(self):
        return self.key().name().split('oclient_')[:-1]
    
    
class OAUTH_Token(db.Model):
    """Save the token used by another applications trying to get the authorization for a user""" 
    #token_key is the Model's key_name field
    token_secret = db.TextProperty()
    token_callback = db.URLProperty(required=False)
    token_verifier = db.TextProperty(required=False)
    access = db.BooleanProperty(default=False)  # True if token is access token
    oauth_user = db.ReferenceProperty(User, required=False)
    oauth_consumer = db.ReferenceProperty(OAUTH_Client)  # the application requesting access
    created = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def token_key(self):
        return self.key().name().split('otoken_')[:-1]
    
    @classmethod
    def generate(cls, *args, **kwargs):
        def _generate_key():
            #genera una cadena de numeros aleatoria, se codifica a base64 y se limpia para URLs
            u = uuid4()
            return base64.urlsafe_b64encode(u.bytes.encode("base64")).strip('=')
        kwargs['key_name'] = 'otoken_%s' % _generate_key()
        kwargs['token_secret'] = _generate_key()
        token = OAUTH_Token(*args, **kwargs)
        token.put()
        return token
    
    def authorize_token(self, user):
        if self.access or self.token_verifier is not None:
            raise OAUTHException('Invalid token')
        self.oauth_user = user
        self.token_verifier = base64.urlsafe_b64encode(uuid4().bytes.encode("base64")).strip('=')
        self.put()
    
    @classmethod
    def get_token(cls, key_name):
        return OAUTH_Token.get_by_key_name('otoken_%s' % key_name)  
        
class OAUTH_Access(db.Model):
    token_secret = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now=True, indexed=False)
    provider = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    
    @property
    def token_key(self):
        return self.key().name().split('atoken_')[1]
    
    @staticmethod
    def remove_token(user, provider):
        tokens = OAUTH_Access.gql('WHERE user = :1 AND provider = :2', user.key(), provider)
        for token in tokens:
            token.delete()
            
    @classmethod
    def add_token(cls, key_name=None, **kwargs):
        """USE THIS METHOD TO CREATE A NEW TOKEN, USE KEY_NAME = None"""
        if key_name is None:
            key_name = 'atoken_%s' % kwargs['token_key']
        
        return OAUTH_Access.get_or_insert(key_name, **kwargs)
    
    @classmethod
    def get_token(cls, key_name):
        return OAUTH_Access.get_by_key_name('atoken_%s' % key_name) 
    
    @classmethod
    def get_token_user(cls, provider, user):
        return OAUTH_Access.all().filter('provider =', provider).filter('user =', user).get()
