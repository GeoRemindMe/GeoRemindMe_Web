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
    url_credentials = 'https://twitter.com/account/verify_credentials.json/'
    url_friends = 'http://api.twitter.com/1/friends/ids.json/'
    url_user_info = 'http://api.twitter.com/1/users/show.json/'
    url_statuses_update = 'https://api.twitter.com/1/statuses/update.json/' 
    user = None
    
    def __init__(self, token=None, user=None):
        if user is None and token is None:
            raise AttributeError
        if user is not None:
            self.user = user
            access_token = OAUTH_Access.get_token_user(provider='twitter', user=user)
            if access_token is None:
                raise OAUTHException()
            token= Token(access_token.token_key, access_token.token_secret)
        consumer = Consumer(key=settings.OAUTH['twitter']['app_key'], secret=settings.OAUTH['twitter']['app_secret'])
        from mapsServices.places.GPRequest import Client
        mem = Client()
        super(self.__class__, self).__init__(consumer, token=token, cache=mem)
    
    def get_user_info(self):
        """Obtiene la infomacion del perfil del usuario"""
        return simplejson.loads(self._do_request(self.url_credentials))
            
    def get_other_user_info(self, id):
        return simplejson.loads(self._do_request(self.url_user_info+'?user_id=%s' % id))
    
    def _do_request(self, url):
        response, content = self.request(url)
        if response['status'] == 400: # no tenemos permisos, borrar usuario
            OAUTH_Access.remove_token(self.user, 'twitter')
            if self.user.twitter_user is not None:
                self.user.twitter_user.delete()
            raise TwitterAPIError(response['status'], content)
        if response['status'] != 200:
            raise TwitterAPIError(response['status'], content)
        return content
        
    def get_friends(self, rpc=None):
        twitterInfo = self.get_user_info()
        if rpc is not None:
            from geouser.models import urlfetch
            return urlfetch.make_fetch_call(rpc, self.url_friends + '?user_id=%s&screen_name=%s' % (
                                                       twitterInfo['id'], 
                                                       twitterInfo['screen_name']
                                                       ),
                                            method='GET'
                                            )
        return self._do_request(self.url_friends + '?user_id=%s&screen_name=%s' % (
                                                                       twitterInfo['id'], 
                                                                       twitterInfo['screen_name']
                                                                       ))
    
    def get_friends_to_follow(self, rpc=None):
        from geouser.models_social import TwitterUser
        if rpc is not None:
            self.get_friends(rpc=rpc)
            return rpc
        ids = self.get_friends()
        registered = []
        for i in ids:
            user_to_follow = TwitterUser.objects.get_by_id(i)
            if user_to_follow is not None and user_to_follow.user.username is not None and not self.user.is_following(user_to_follow.user):
                info = self.get_others_user_info(id=user_to_follow.id)
                registered[user_to_follow.user.id] = { 
                                               'username': user_to_follow.user.username, 
                                               'twittername': info['screen_name'],
                                               'id': user_to_follow.user.id,
                                               }
        return registered
    def authorize(self, user = None, login=True):
        if self.user is None:
            if user is None:
                raise TypeError
            self.user = user
        """Guarda el token de autorizacion"""
        if self.user is not None:#el usuario ya esta conectado, pero pide permisos
            if OAUTH_Access.get_token(self.token.key) is None: 
                OAUTH_Access.remove_token(self.user, 'twitter')
                access = OAUTH_Access.add_token(
                                                token_key=self.token.key,
                                                token_secret=self.token.secret,
                                                provider='twitter',
                                                user=self.user,
                                                )
            if login:
                twitterInfo = self.get_user_info()
                if self.user.twitter_user is None:
                    TwitterUser.register(user=self.user,
                                     uid=twitterInfo['id'], 
                                     username = twitterInfo['screen_name'],
                                     realname = twitterInfo['name'],
                                     picurl = twitterInfo['profile_image_url'],
                                     )
                else:
                    self.user.twitter_user.update(
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
            self.user = user.user
            auth = self.authorize()
            if not auth:
                raise AttributeError
        else:#no existe, creamos un nuevo usuario
            self.user = User.register(password=make_random_string(length=6), confirmed=True)
            self.user.settings.sync_avatar_with = 'twitter' #  por defecto, si el usuario es nuevo sincronizamos con facebook
            self.user.settings.put()
            self.authorize(user)
        return self.user
    
    def send_tweet(self, msg, poi=None, wrap_links=False):
        body = {
                'status': msg.encode('utf-8'),
                }
        if poi is not None:
            body['lat'] = poi.lat
            body['lon'] = poi.lon
        body['wrap_links'] = 'true' if wrap_links else 'false'
        from urllib import urlencode
        response, content = self.request(self.url_statuses_update, method='POST', body=urlencode(body))
        if response['status'] != 200:
            raise TwitterAPIError(response['status'], response)
        return simplejson.loads(content)
        
class TwitterFriendsRPC(object):
    def fetch_friends(self, user):
        from geouser.models import urlfetch
        self.rpc = urlfetch.create_rpc(callback=self.handle_results)
        self.user = user
        self.friends = {}
        try:
            twclient = TwitterClient(user=user)
            self.rpc = twclient.get_friends_to_follow(rpc=self.rpc)
        except:
            return None
        return self.rpc
    
    def handle_results(self):
        result = self.rpc.get_result()
        from django.utils import simplejson
        if int(result.status_code) != 200:
            return {}
        friends_result = simplejson.loads(result.content)
        if len(friends_result) == 0:
            return {}
        friends_key = ['tu%s' % f for f in friends_result]
        users_to_follow = TwitterUser.get_by_key_name(friends_key)
        users_to_follow = filter(None, users_to_follow)
        for user_to_follow in users_to_follow:
            if user_to_follow.user.username is not None and \
                not self.user.is_following(user_to_follow.user):
                    info = self.get_others_user_info(id=user_to_follow.id)
                    self.friends[user_to_follow.user.id] = { 
                                               'username': user_to_follow.user.username, 
                                               'twittername': info['screen_name'],
                                               'id': user_to_follow.user.id,
                                               }
        return self.friends
        
