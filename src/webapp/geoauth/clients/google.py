# coding=utf-8

from django.conf import settings
from libs.oauth2 import Client, Consumer
from geoauth.models import OAUTH_Access
from geoauth.exceptions import OAUTHException


class GoogleClient(Client):
    _source='Georemindme-v0.1'
    _client = None
    
    def __init__(self, token=None, user=None):
        if user is not None:
            self.user = user
        consumer = Consumer(key=settings.OAUTH['google']['app_key'], secret=settings.OAUTH['google']['app_secret'])
        super(self.__class__, self).__init__(consumer, token=token)
    
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
        from libs.gdata.contacts.client import ContactsClient
        from libs.gdata.gauth import OAuthHmacToken, ACCESS_TOKEN
        
        from django.conf import settings
        token = OAUTH_Access.get_token_user(provider='google', user=self.user)
        if token is not None:
            self._client = ContactsClient(source=self._source)
            self._client.auth_token = OAuthHmacToken(settings.OAUTH['google']['app_key'],
                                           settings.OAUTH['google']['app_secret'],
                                           token.token_key,
                                           token.token_secret, 
                                           ACCESS_TOKEN
                                           )
        else:
            raise OAUTHException
        #from libs.gdata.alt.appengine import run_on_appengine
        #run_on_appengine(self._client)
        
    def get_contacts(self):
        return self._client.GetContacts()
    
    def get_contacts_to_follow(self):
        from geouser.models import User
        registered = []
        feed = self.get_contacts()
        for i, entry in enumerate(feed.entry):
            for email in entry.email:
                user = User.objects.get_by_email(email.address)
                if user is not None:
                    registered.append({'id':user.id, 
                                       'username': user.username, 
                                       'avatar': user.profile.avatar, 
                                       'email': user.email
                                       })
        return registered