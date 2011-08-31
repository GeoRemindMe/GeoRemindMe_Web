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
        
    def get_contacts(self, rpc=None):
        request = self._client.GetContacts(rpc=rpc)
        if rpc is not None:
            from geouser.models import urlfetch
            return urlfetch.make_fetch_call(rpc, str(request.uri), headers=request.headers)
        return request
    
    def get_contacts_to_follow(self, rpc=None):
        from geouser.models import User
        registered = []
        if rpc is not None:
            self.get_contacts(rpc=rpc)
            return rpc
        feed = self.get_contacts()
        for i, entry in enumerate(feed.entry):
            for email in entry.email:
                user_to_follow = User.objects.get_by_email(email.address)
                if user_to_follow is not None and user_to_follow.username is not None and not self.user.is_following(user_to_follow):
                    registered[user_to_follow.id]={ 
                                                'username': user_to_follow.username, 
                                                'email': user_to_follow.email,
                                                'id': user_to_follow.user.id,
                                                }
        return registered
    
    
class GoogleFriendsRPC(object):
    def fetch_friends(self, user):
        from geouser.models import urlfetch
        self.rpc = urlfetch.create_rpc(callback=self.handle_results)
        self.user = user
        self.friends = {}
        try:
            goclient = GoogleClient(user=user)
            self.rpc = goclient.get_contacts_to_follow(rpc=self.rpc)
            
        except:
            return None
        return self.rpc
    
    def handle_results(self):
        result = self.rpc.get_result()
        from django.utils import simplejson
        if result.status_code != 200:
            return {}
        # recibimos en xml, parsear resultado
        from libs.atom.core import parse
        from libs.gdata.contacts.data import ContactsFeed
        contacts = parse(result.content, ContactsFeed,)
        for i, entry in enumerate(contacts.entry):
            for email in entry.email:
                from geouser.models import User
                user_to_follow = User.objects.get_by_email(email.address)
                if user_to_follow is not None and user_to_follow.username is not None and not self.user.is_following(user_to_follow):
                    self.friends[user_to_follow.id]={ 
                                                'username': user_to_follow.username, 
                                                'email': user_to_follow.email,
                                                'id': user_to_follow.user.id,
                                                }
        return self.friends