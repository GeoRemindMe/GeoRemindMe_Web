# coding=utf-8

from django.conf import settings
from geoauth.clients.facebook import get_user_from_cookie, parse_signed_request, FacebookClient


class FacebookCSRFMiddleware(object):
    def process_request(self, request):
        if 'signed_request' in request.REQUEST:
            try:
                data = parse_signed_request(request.REQUEST['signed_request'])
                request.method = 'GET'
                request.csrf_processing_done = True
            except:
                pass
        else:
            cookie = get_user_from_cookie(request.COOKIES)
            if cookie is not None:
                request.csrf_processing_done = True
        request.csrf_processing_done = False


class FacebookMiddleware(object):
    def process_request(self, request):
        if 'signed_request' in request.REQUEST:
            data = parse_signed_request(request.REQUEST['signed_request'])
            if 'oauth_token' in data:
                request.facebook = {'uid': data['user_id'],
                                    'access_token': data['oauth_token'],
                                    'client': FacebookClient(access_token=data['oauth_token'])
                                    }
        else:
            cookie = get_user_from_cookie(request.COOKIES)
            if cookie is not None:
                try:
                    request.facebook = {'uid': cookie['uid'],
                                        'access_token': cookie['access_token'],
                                        'client': FacebookClient(access_token=cookie['access_token'])
                                    }
                    
                except:
                    pass
        if not hasattr(request, 'facebook'):
            from facebookApp.watchers import disconnect_all
            disconnect_all()
        else:
            if request.user.is_authenticated():
                if request.facebook['client'].user is not None:
                    if request.facebook['client'].user.id != request.user.id or request.facebook['uid'] != request.user.facebook_user.uid:
                        # son usuarios distintos, cerramos la sesion del viejo usuario conectado
                        request.session.delete()
                        request.session.init_session(user=request.facebook['client'].user, is_from_facebook=True)
                        request.user = request.facebook['client'].user
                        from facebookApp.watchers import new_comment, new_vote, deleted_post
            else:
                if request.facebook['client'].user is not None:
                    # login desde facebook de un usuario conocido
                    request.session.delete()
                    request.session.init_session(user=request.facebook['client'].user, is_from_facebook=True)
                    request.user = request.facebook['client'].user
                    from facebookApp.watchers import new_comment, new_vote, deleted_post
