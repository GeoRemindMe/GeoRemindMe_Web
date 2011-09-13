# coding=utf-8

#
# Copyright 2010 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Python client library for the Facebook Platform.

This client library is designed to support the Graph API and the official
Facebook JavaScript SDK, which is the canonical way to implement
Facebook authentication. Read more about the Graph API at
http://developers.facebook.com/docs/api. You can download the Facebook
JavaScript SDK at http://github.com/facebook/connect-js/.

If your application is using Google AppEngine's webapp framework, your
usage of this module might look like this:

    user = facebook.get_user_from_cookie(self.request.cookies, key, secret)
    if user:
        graph = facebook.GraphAPI(user["access_token"])
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")

"""

import cgi
import time
import urllib
import hashlib
import hmac
import base64
import logging
from django.conf import settings
import libs.httplib2 as httplib2
# Find a JSON parser
from django.utils import simplejson as json
_parse_json = json.loads

from geoauth.models import OAUTH_Access
from geoauth.exceptions import OAUTHException
from geouser.models import User
from geouser.models import urlfetch
from geouser.models_social import FacebookUser
from georemindme.funcs import make_random_string


class FacebookClient(object):
    _fb_id = None
    user = None
    consumer = None 
        
    def __init__(self, access_token=None, user=None):
        if user is None and access_token is None:
            raise AttributeError
        import memcache
        memclient = memcache.mem.Client()
        if user is not None:
            token = memcache.deserialize_instances(memclient.get('%sfbclientuser_%s' % (memcache.version, 
                                                                  user.id
                                                                  )
                                               ))
            if token is None:
                token = OAUTH_Access.get_token_user(provider='facebook', user=user)
                if token is None:
                    raise OAUTHException()
                memclient.set('%sfbclientuser_%s' % (memcache.version, 
                                                                  user.id
                                                                  ),
                               memcache.serialize_instances(token)
                                               )
        else:
            token = memclient.get('%sfbclienttoken_%s' % (memcache.version, 
                                                                  access_token
                                                                  )
                                               )
            if token is None:
                token = OAUTH_Access.get_token(access_token)  # TODO: buscar por proveedor
                if token is not None:
                    user = token.user
                    token_cache = {'token': token,
                                   'user': user
                                   }
                    memclient.set('%sfbclienttoken_%s' % (memcache.version, 
                                                          access_token
                                                  ), token_cache)
                else:
                    self.consumer = GraphAPI(access_token=access_token)
                    return
            else:
                user = token['user']
                token = token['token']
        self.user = user
        self.consumer = GraphAPI(access_token=token.token_key)
    
    def get_user_info(self): 
        """
        It returns a dictionary with this keys:
        - first_name
        - last_name
        - verified'
        - name
        - locale
        - gender
        - email
        - link: profile link
        - timezone: GMT+VAR
        - updated_time
        - id: 100002508846747
        """
   
        me = self.consumer.get_object("me")
        self._fb_id = me['id']
        return me
    
    def get_friends(self, rpc=None):
        if self._fb_id is None:
            self.get_user_info()
        friends = self.consumer.get_connections(self._fb_id, "friends", rpc=rpc)
        return friends
    
    def get_friends_to_follow(self, rpc=None):
        """Devuelve un array de amigos con id, username, avatar, uid"""
        if rpc is not None:
            self.get_friends(rpc=rpc)
            return rpc
        friends = self.get_friends()
        friends = friends['data']
        registered = {}
        for f in friends:
            user_to_follow = FacebookUser.objects.get_by_id(f['id'])
            if user_to_follow is not None and user_to_follow.user.username is not None and not self.user.is_following(user_to_follow.user):
                registered[user_to_follow.user.id]= {
                                                   'username':user_to_follow.user.username, 
                                                   'uid':user_to_follow.uid,
                                                   'id': user_to_follow.user.id,
                                                   }
        return registered
        
    def authorize(self, user):
        """guarda el token de autorizacion"""
        if user is not None:#el usuario ya esta conectado, pero pide permisos
            if OAUTH_Access.get_token(self.consumer.access_token,) is None: 
                OAUTH_Access.remove_token(user, 'facebook')
                self.token = OAUTH_Access.add_token(
                                                token_key=self.consumer.access_token,
                                                token_secret='',
                                                provider='facebook',
                                                user=user,
                                                )
            facebookInfo = self.get_user_info()
            if user.facebook_user is None:
                fbuser = FacebookUser.register(user=user, uid=facebookInfo['id'], 
                                               email=facebookInfo['email'], realname=facebookInfo["name"],
                                               profile_url=facebookInfo["link"],
                                               access_token=self.consumer.access_token)
            else:
                user.facebook_user.update(
                             realname = facebookInfo['name'],
                             profile_url=facebookInfo["link"]
                            )
            self.user = user
            import memcache
            memclient = memcache.mem.Client()
            token_cache = {'token': self.token,
                                   'user': self.user
                                   }
            memclient.set('%sfbclienttoken_%s' % (memcache.version, 
                                                  self.consumer.access_token
                                                  ), token_cache)
            return True
        return False
    
    def authenticate(self,password=None):
        """el usuario se esta logeando usando facebook"""
        try:
            facebookInfo = self.get_user_info()
        except:
            return False
        fbuser = FacebookUser.objects.get_by_id(facebookInfo['id'])
        if fbuser is not None:#el usuario ya existe, iniciamos sesion
            self.user = fbuser.user
        else:#no existe, creamos un nuevo usuario
            self.user = User.objects.get_by_email(facebookInfo['email'])
            if self.user is None:
                self.user = User.register(email=facebookInfo['email'], password=password if password is not None else make_random_string(length=6))
                self.user.profile.sync_avatar_with = 'facebook' #  por defecto, si el usuario es nuevo sincronizamos con facebook
                self.user.profile.put()
        self.authorize(self.user)
        return self.user
    
    def token_is_valid(self):
        """el usuario se esta logeando usando facebook"""
        try:
            facebookInfo = self.get_user_info()
            return True
        except:
            return False
        
        
class FacebookFriendsRPC(object):
    def fetch_friends(self, user):
        from geouser.models import urlfetch
        self.rpc = urlfetch.create_rpc(callback=self.handle_results)
        self.user = user
        self.friends = {}
        try:
            fbclient = FacebookClient.load_client(user=user)
            self.rpc = fbclient.get_friends_to_follow(rpc=self.rpc)
        except:
            return None
        return self.rpc
    
    def handle_results(self):
        result = self.rpc.get_result()
        from django.utils import simplejson
        from geouser.models_social import FacebookUser
        if result.status_code != 200:
            return {}
        friends_result = simplejson.loads(result.content)
        if 'data' in friends_result:
            friends_result = friends_result['data']
        for f in friends_result:
            user_to_follow = FacebookUser.objects.get_by_id(f['id'])
            if user_to_follow is not None and user_to_follow.user.username is not None and not self.user.is_following(user_to_follow.user):
                self.friends[user_to_follow.user.id]= {
                                           'username':user_to_follow.user.username, 
                                           'uid':user_to_follow.uid,
                                           'id': user_to_follow.user.id,
                                           }
        return self.friends
        

class GraphAPI(object):
    """A client for the Facebook Graph API.

    See http://developers.facebook.com/docs/api for complete documentation
    for the API.

    The Graph API is made up of the objects in Facebook (e.g., people, pages,
    events, photos) and the connections between them (e.g., friends,
    photo tags, and event RSVPs). This client provides access to those
    primitive types in a generic way. For example, given an OAuth access
    token, this will fetch the profile of the active user and the list
    of the user's friends:

       graph = facebook.GraphAPI(access_token)
       user = graph.get_object("me")
       friends = graph.get_connections(user["id"], "friends")

    You can see a list of all of the objects and connections supported
    by the API at http://developers.facebook.com/docs/reference/api/.

    You can obtain an access token via OAuth or by using the Facebook
    JavaScript SDK. See http://developers.facebook.com/docs/authentication/
    for details.

    If you are using the JavaScript SDK, you can use the
    get_user_from_cookie() method below to get the OAuth access token
    for the active user from the cookie saved by the SDK.
    """
    def __init__(self, access_token=None):
        from mapsServices.places.GPRequest import Client
        mem = Client()
        self.req = httplib2.Http(cache=mem)
        self.access_token = access_token

    def get_object(self, id, **args):
        """Fetchs the given object from the graph."""
        return self.request(id, args)

    def get_objects(self, ids, **args):
        """Fetchs all of the given object from the graph.

        We return a map from ID to object. If any of the IDs are invalid,
        we raise an exception.
        """
        args["ids"] = ",".join(ids)
        return self.request("", args)

    def get_connections(self, id, connection_name, rpc=None, **args):
        """Fetchs the connections for given object."""
        return self.request(id + "/" + connection_name, args, rpc=rpc)

    def put_object(self, parent_object, connection_name, **data):
        """Writes the given object to the graph, connected to the given parent.

        For example,

            graph.put_object("me", "feed", message="Hello, world")

        writes "Hello, world" to the active user's wall. Likewise, this
        will comment on a the first post of the active user's feed:

            feed = graph.get_connections("me", "feed")
            post = feed["data"][0]
            graph.put_object(post["id"], "comments", message="First!")

        See http://developers.facebook.com/docs/api#publishing for all of
        the supported writeable objects.

        Most write operations require extended permissions. For example,
        publishing wall posts requires the "publish_stream" permission. See
        http://developers.facebook.com/docs/authentication/ for details about
        extended permissions.
        """
        #~ if connection_name == "feed":
            #~ raise Exception("%s/%s %s" % (parent_object,connection_name, data))
        assert self.access_token, "Write operations require an access token"
        return self.request(parent_object + "/" + connection_name, post_args=data)

    def put_wall_post(self, message, attachment={}, profile_id="me"):
        """Writes a wall post to the given profile's wall.

        We default to writing to the authenticated user's wall if no
        profile_id is specified.

        attachment adds a structured attachment to the status message being
        posted to the Wall. It should be a dictionary of the form:

            {"name": "Link name",
             "link": "http://www.example.com/",
             "caption": "{*actor*} posted a new review",
             "description": "This is a longer description of the attachment",
             "picture": "http://www.example.com/thumbnail.jpg"}

        """
        return self.put_object(profile_id, "feed", message=message, **attachment)

    def put_comment(self, object_id, message):
        """Writes the given comment on the given post."""
        return self.put_object(object_id, "comments", message=message)

    def put_like(self, object_id):
        """Likes the given post."""
        return self.put_object(object_id, "likes")

    def delete_object(self, id):
        """Deletes the object with the given ID from the graph."""
        self.request(id, post_args={"method": "delete"})


    def put_photo(self, image, message=None, album_id=None, **kwargs):
        """
        Shortcut for put_media to upload a photo
        """
        self.put_media(image, message, album_id, fxtype='photos', kwargs=kwargs)

    def put_video(self, image, message=None, album_id=None, **kwargs):
        """
        Shortcut for put_media to upload a video
        """
        self.put_media(image, message, album_id, fxtype='videos', kwargs=kwargs)

    def put_media(self, fx, message=None, album_id=None, fxtype=None, **kwargs):
        """Uploads a file using multipart/form-data
        fx: File like object for the image
        message: Caption for your image
        album_id: On photos, None posts to /me/photos which uses or creates and uses 
        an album for your application.
        fxtype: one of 'photos' or 'videos' depending on media type
        """
        object_id = album_id or "me"
        #it would have been nice to reuse self.request; but multipart is messy in urllib
        post_args = {
				  'access_token': self.access_token,
				  'source': fx,
				  'message': message
        }
        post_args.update(kwargs)
        
        content_type, body = self._encode_multipart_form(post_args, fxtype)
        headers = {'Content-Type' : content_type}
        response, content = self.req.request(self, "https://graph.facebook.com/%s/%s" % (object_id, fxtype),
                                                  method='POST', body=body, headers=headers)
        data = _parse_json(content)
        if response['status'] != 200:
            raise GraphAPIError(response["error"].get("code", 1),
                                response["error"]["message"])
        return response

    # based on: http://code.activestate.com/recipes/146306/
    def _encode_multipart_form(self, fields, fxtype):
        """Fields are a dict of form name-> value
        For files, value should be a file object.
        Other file-like objects might work and a fake name will be chosen.
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.items():
            logging.debug("Encoding %s, (%s)%s" % (key, type(value), value))
            if not value:
                continue
            L.append('--' + BOUNDARY)
            if hasattr(value, 'read') and callable(value.read): 
                filename = str(getattr(value,'name','%s.jpg' % key))
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
                if fxtype == "videos":
                    L.append('Content-Type: video/*')    
                else:
                    L.append('Content-Type: image/*')
                value = value.read()
                logging.debug(type(value))
            else:
                L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            if isinstance(value, unicode):
                logging.debug("Convert to ascii")
                value = value.encode('ascii')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def request(self, path, args=None, post_args=None, rpc=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        post_data = None if post_args is None else urllib.urlencode(post_args) 
        if rpc is not None:
            return urlfetch.make_fetch_call(rpc, "https://graph.facebook.com/" + path + "?" +
                                            urllib.urlencode(args), 
                                            method='GET' if post_data is None else 'POST',
                                            payload=post_data)
                 
        response, content = self.req.request("https://graph.facebook.com/" + path + "?" +
                                            urllib.urlencode(args), 
                                            method='GET' if post_data is None else 'POST',
                                            body=post_data)
        content = _parse_json(content)
        if response['status'] != 200:
            raise GraphAPIError(content["error"]["type"],
                                content["error"]["message"])
        if response['content-type'].startswith('text'):
            return content
        if response['content-type'].startswith('image'):
            content = {
                "data": content,
                "mime-type": response['content-type'],
                "url": response['url'],
            }
        raise GraphAPIError('Response Error', 'Maintype was not text or image')
        

    def api_request(self, path, args=None, post_args=None):
        """Fetches the given path in the Graph API.

        We translate args to a valid query string. If post_args is given,
        we send a POST request to the given path with the given arguments.
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        if self.api_key:
            if post_args is not None:
                post_args["api_key"] = self.api_key
            else:
                args["api_key"] = self.api_key
        if post_args is not None:
            post_args["format"] = "json-strings"
        else:
            args["format"] = "json-strings"
        post_data = None if post_args is None else urllib.urlencode(post_args)
        response, content = self.req.request("https://api.facebook.com/" + path + "?" +
                                            urllib.urlencode(args),
                                            method='GET' if post_data is None else 'POST',
                                            body=post_data)
        content = _parse_json(content)
        if response['status'] != 200:
            raise GraphAPIError(content["error"]["type"],
                                content["error"]["message"])
        return content
        

    def fql(self, query, args=None, post_args=None):
        """FQL query.
        Two reasons to have this method:
        1. Graph api does not expose some info fields of a user, e.g.
            a user's networks/affiliations, we have to fall back to old api.
        2. FQL is a strong tool.
        Example query: "SELECT affiliations FROM user WHERE uid = me()"
        """
        if not args: args = {}
        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token
        post_data = None if post_args is None else urllib.urlencode(post_args)

        args["query"] = query
        args["format"]="json"
        response, content = self.req.request("https://api.facebook.com/method/fql.query?" + 
                                            urllib.urlencode(args),
                                            method='GET' if post_data is None else 'POST',
                                            body=post_data)
        content = _parse_json(content)
        if response['status'] != 200:
            raise GraphAPIError(content["error_code"],content["error_msg"])
        return content


class GraphAPIError(Exception):
    def __init__(self, type, message):
        Exception.__init__(self, message)
        self.type = type

def get_user_from_cookie(cookies, app_id=settings.OAUTH['facebook']['app_key'], app_secret=settings.OAUTH['facebook']['app_secret']):
    """Parses the cookie set by the official Facebook JavaScript SDK.

    cookies should be a dictionary-like object mapping cookie names to
    cookie values.

    If the user is logged in via Facebook, we return a dictionary with the
    keys "uid" and "access_token". The former is the user's Facebook ID,
    and the latter can be used to make authenticated requests to the Graph API.
    If the user is not logged in, we return None.

    Download the official Facebook JavaScript SDK at
    http://github.com/facebook/connect-js/. Read more about Facebook
    authentication at http://developers.facebook.com/docs/authentication/.
    """
    cookie = cookies.get("fbs_" + app_id, "")
    if not cookie: return None
    args = dict((k, v[-1]) for k, v in cgi.parse_qs(cookie.strip('"')).items())
    payload = "".join(k + "=" + args[k] for k in sorted(args.keys())
                      if k != "sig")
    sig = hashlib.md5(payload + app_secret).hexdigest()
    expires = int(args["expires"])
    if sig == args.get("sig") and (expires == 0 or time.time() < expires):
        return args
    else:
        return None

def parse_signed_request(signed_request, app_secret=settings.OAUTH['facebook']['app_secret']):
    """Return dictionary with signed request data."""
    try:
        l = signed_request.split('.', 2)
        encoded_sig = str(l[0])
        payload = str(l[1])
    except IndexError:
        raise ValueError("'signed_request' malformed")
    
    sig = base64.urlsafe_b64decode(encoded_sig + "=" * ((4 - len(encoded_sig) % 4) % 4))
    data = base64.urlsafe_b64decode(payload + "=" * ((4 - len(payload) % 4) % 4))

    data = _parse_json(data)

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        raise ValueError("'signed_request' is using an unknown algorithm")
    else:
        expected_sig = hmac.new(app_secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        raise ValueError("'signed_request' signature mismatch")
    else:
        return data
  
def auth_url(app_id, canvas_url, perms = None):
    url = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s" % (app_id, canvas_url)
    if perms:
        url += "scope=%s" % (",".join(perms))
    return url

def get_app_access_token():
    
    """
    Get the access_token for the app that can be used for insights and creating test users
    application_id = retrieved from the developer page
    application_secret = retrieved from the developer page
    returns the application access_token
    """
    # Get an app access token
    args = {'grant_type':'client_credentials',
            'client_id': settings.OAUTH['facebook']['app_key'],
            'client_secret':settings.OAUTH['facebook']['app_secret']}
    
    request = httplib2.Http()
    response, content = request.request("https://graph.facebook.com/oauth/access_token?" + 
                                            urllib.urlencode(args))
    if response['status'] != 200:
        raise GraphAPIError(content["error_code"],content["error_msg"])
    result = content.split("=")[1]
    return result

def add_test_users():
    access_token = get_app_access_token()
    request = httplib2.Http()
    args = {
            'permissions': settings.OAUTH['facebook']['scope'],
            'access_token': access_token,
            }
    
    response, content = request.request("https://graph.facebook.com/%s/accounts/test-users?installed=true&method=post&" % settings.OAUTH['facebook']['app_key'] +
                                        urllib.urlencode(args),
                                        )
    
    if response['status'] != 200:
        raise GraphAPIError(response, content)
    return content

def get_test_users():
    access_token = get_app_access_token()
    request = httplib2.Http()
    response, content = request.request("https://graph.facebook.com/%s/accounts/test-users?access_token=%s" % (settings.OAUTH['facebook']['app_key'], access_token))
    
    if response['status'] != 200:
        raise GraphAPIError(response, content)
    return content
