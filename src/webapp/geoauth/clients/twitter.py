# coding=utf-8
from django.utils import simplejson
from django.conf import settings
from libs.oauth2 import Client, Consumer

from google.appengine.ext import db
from geoauth.models import OAUTH_Access
from geouser.models import User
from geouser.models_social import TwitterUser
from georemindme.funcs import make_random_string


class TwitterClient(Client):
    url_credentials = 'https://twitter.com/account/verify_credentials.json'
    
    def __init__(self, token=None):
        consumer = Consumer(key=settings.OAUTH['twitter']['app_key'], secret=settings.OAUTH['twitter']['app_secret'])
        super(self.__class__, self).__init__(consumer, token=token)
    
    def get_user_info(self):
        """Obtiene la infomacion del perfil del usuario"""
        response, content = self.request('https://twitter.com/account/verify_credentials.json')
        return simplejson.loads(content)
        
    
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
                user.twitter_user.update(username = twitterInfo['screen_name'],
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
