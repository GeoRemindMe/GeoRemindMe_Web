# coding=utf-8
from django.utils import simplejson
from django.conf import settings
from libs.oauth2 import Client, Consumer, Token

from geoauth.models import OAUTH_Access
from geoauth.exceptions import OAUTHException
from geouser.models import User
from geouser.models_social import TwitterUser
from georemindme.funcs import make_random_string

class TwitterAPIError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type

class TwitterClient(Client):
    url_credentials = 'https://twitter.com/account/verify_credentials.json'
    url_friends = 'http://api.twitter.com/version/friends/ids.json'
    
    def __init__(self, token=None, user=None):
        if user is not None:
            self.user = user
            access_token = OAUTH_Access.get_token_user(provider='twitter', user=user)
            if access_token is None:
                raise OAUTHException()
            token= Token(access_token.token_key, access_token.token_secret)
        consumer = Consumer(key=settings.OAUTH['twitter']['app_key'], secret=settings.OAUTH['twitter']['app_secret'])
        super(self.__class__, self).__init__(consumer, token=token)
    
    def get_user_info(self):
        """Obtiene la infomacion del perfil del usuario"""
        
        response, content = self.request('https://twitter.com/account/verify_credentials.json')
        if response['status'] != 200:
            raise TwitterAPIError(response['status'], response)
        return simplejson.loads(content)
    
    def get_other_user_info(self, id):
        response, content = self.request('http://api.twitter.com/1/users/show.json/?user_id=%s' % id)
        if response['status'] != 200:
            raise TwitterAPIError(response['status'], response)
        return simplejson.loads(content)
    
    
    def get_friends(self):
        twitterInfo = self.get_user_info()
        response, content = self.request(
                                        'http://api.twitter.com/1/friends/ids.json/?user_id=%s&screen_name=%s' % (
                                                                       twitterInfo['id'], 
                                                                       twitterInfo['screen_name']
                                                                       ),
                                         method='GET'
                                         )
        if response['status'] != 200:
            raise TwitterAPIError(response['status'], content)
        return content
    
    def get_friends_to_follow(self):
        from geouser.models_social import TwitterUser
        ids = self.get_friends()
        registered = []
        for i in ids:
            user = TwitterUser.objects.get_by_id(i)
            if user is not None:
                info = self.get_others_user_info(id=user.id)
                registered.append({'id':user.id, 
                                   'username': user.username, 
                                   'avatar': user.profile.avatar,
                                   'twittername': info['screen_name'], 
                                   })
        return registered
    def authorize(self, user=None):
        """Guarda el token de autorizacion"""
        if user is not None:#el usuario ya esta conectado, pero pide permisos
            if OAUTH_Access.get_token(self.token.key) is None: 
                OAUTH_Access.remove_token(user, 'twitter')
                access = OAUTH_Access.add_token(
                                                token_key=self.token.key,
                                                token_secret=self.token.secret,
                                                provider='twitter',
                                                user=user,
                                                )
            twitterInfo = self.get_user_info()
            if user.twitter_user is None:
                TwitterUser.register(user=user,
                                 uid=twitterInfo['id'], 
                                 username = twitterInfo['screen_name'],
                                 realname = twitterInfo['name'],
                                 picurl = twitterInfo['profile_image_url'],
                                 )
            else:
                user.twitter_user.update(
                                         username = twitterInfo['screen_name'],
                                         realname = twitterInfo['name'],
                                         picurl = twitterInfo['profile_image_url']
                                         )
            return True
        return False
    
    def authenticate(self):
        """Permite al usuario loguear con twitter"""
        twitterInfo = self.get_user_info()
        user = TwitterUser.objects.get_by_id(twitterInfo['id'])
        if user is not None:#el usuario ya existe, iniciamos sesion
            user = user.user
            self.authorize(user)
        else:#no existe, creamos un nuevo usuario
            user = User.register(password=make_random_string(length=6))
            self.authorize(user)
        return user
