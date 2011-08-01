# coding=utf-8

from django.conf import settings
from libs.oauth2 import Client, Consumer, Token
from geoauth.models import OAUTH_Access
from geoauth.exceptions import OAUTHException


class GoogleClient(Client):
    _source='Georemindme-v0.1 www.georemindme.com'
    _client = None
    
    def __init__(self, token=None, user=None):
        if user is None and token is None:
            raise AttributeError
        
        from libs.gdata.contacts.client import ContactsClient
        from libs.gdata.gauth import OAuthHmacToken, ACCESS_TOKEN
        if user is not None:
            self.user = user
            access_token = OAUTH_Access.get_token_user(provider='google', user=self.user)
            if access_token is not None:
                token= Token(access_token.token_key, access_token.token_secret)
            else:
                raise OAUTHException
        consumer = Consumer(key=settings.OAUTH['google']['app_key'], secret=settings.OAUTH['google']['app_secret'])
        super(self.__class__, self).__init__(consumer, token=token)
        
        self._client = ContactsClient(source=self._source)
        self._client.auth_token = OAuthHmacToken(settings.OAUTH['google']['app_key'],
                                           settings.OAUTH['google']['app_secret'],
                                           self.token.key,
                                           self.token.secret, 
                                           ACCESS_TOKEN
                                           )
    
    def authorize(self, user=None):
        """Guarda el token de autorizacion"""
        if user is not None:#el usuario ya esta conectado, pero pide permisos
            if OAUTH_Access.get_token(self.token.key) is None: 
                OAUTH_Access.remove_token(user, 'google')
                access = OAUTH_Access.add_token(
                                                token_key=self.token.key,
                                                token_secret=self.token.secret,
                                                provider='google',
                                                user=user,
                                                )

            return True
        return False
    
    def load_client(self):
        #from libs.gdata.alt.appengine import run_on_appengine
        #run_on_appengine(self._client)
        pass
        
    def get_contacts(self):
        return self._client.GetContacts()
    
    def get_contacts_to_follow(self):
        from geouser.models import User
        registered = []
        feed = self.get_contacts()
        for i, entry in enumerate(feed.entry):
            for email in entry.email:
                user_to_follow = User.objects.get_by_email(email.address)
                if user_to_follow is not None and user_to_follow.username is not None and not self.user.is_following(user_to_follow):
                    registered[user_to_follow.id]={ 
                                                'username': user_to_follow.username, 
                                                'email': user_to_follow.email
                                                }
        return registered