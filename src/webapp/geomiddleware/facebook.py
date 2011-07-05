# coding=utf-8

from django.conf import settings
import base64

class FacebookMiddleware(object):
    def process_request(self, request):
        from geoauth.clients.facebook import FacebookClient, get_user_from_cookie
        if 'signed_request' in request.REQUEST:
            signed_request = request.REQUEST.get('signed_request').split('.')
            if self._check_signature(signed_request[0], signed_request[1]):
                from django.utils import simplejson
                data = simplejson.loads(self._base64_url_decode(signed_request[1]))
                if 'oauth_token' in data:
                    request.facebook = {'uid': data['user_id'],
                                        'access_token': data['oauth_token'],
                                        'client': FacebookClient(data['oauth_token'])
                                        }
                request.csrf_processing_done = True
        else:
            cookie = get_user_from_cookie(request.COOKIES)
            if cookie is not None:
                request.facebook = cookie
                request.facebook['client'] = FacebookClient(cookie["access_token"])
                request.csrf_processing_done = True
            else:  # no es un usuario de facebook, desconectar señales
                from facebookApp.watchers import disconnect_all
                disconnect_all()   
                
    def _base64_url_decode(self, inp):
        # http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "="*padding_factor
        return base64.urlsafe_b64decode(inp.encode('ascii'))


    def _check_signature(self, signature, payload):
        import hmac
        from hashlib import sha256
        sha = sha256
        # Validate the signature.
        valid_key = hmac.new(settings.OAUTH['facebook']['app_secret'], payload, sha)
        valid_key = base64.urlsafe_b64encode(valid_key.digest())[:-1]
        if valid_key == signature:
            return True
        else:
            return False
            
        
    