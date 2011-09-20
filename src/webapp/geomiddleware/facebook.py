# coding=utf-8

from django.conf import settings
from geoauth.clients.facebook import get_user_from_cookie, parse_signed_request, FacebookClient


class FacebookCSRFMiddleware(object):
    def process_request(self, request):
        try:
            if 'signed_request' in request.REQUEST:
                data = parse_signed_request(request.REQUEST['signed_request'])
                request.method = 'GET'
                request.csrf_processing_done = True
            else:
                cookie = get_user_from_cookie(request.COOKIES)
                if cookie is not None:
                    request.csrf_processing_done = True
        except:
            pass
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
        if not hasattr(request, 'facebook'):
                try:
                    cookie = get_user_from_cookie(request.COOKIES)
                    if cookie is not None:
                        request.facebook = {'uid': cookie['user_id'],
                                        'access_token': cookie['oauth_token'],
                                        'client': FacebookClient(access_token=cookie['oauth_token'])
                                    }
                except:
                    pass
        if not hasattr(request, 'facebook'):
            from facebookApp.watchers import disconnect_all
            disconnect_all()
        else:
            if request.user.is_authenticated():
                if request.facebook['client'].user is not None:
                    if request.facebook['client'].user.id != request.user.id:
                        # son usuarios distintos, cerramos la sesion del viejo usuario conectado
                        #request.session.delete()
                        from geouser.funcs import init_user_session
                        init_user_session(request, request.facebook['client'].user, remember=True, is_from_facebook=True)
                        from facebookApp.watchers import new_comment, new_vote, deleted_post
            else:
                if request.facebook['client'].user is not None:
                    # login desde facebook de un usuario conocido
                    from geouser.funcs import init_user_session
                    init_user_session(request, request.facebook['client'].user, remember=True, is_from_facebook=True)
                    from facebookApp.watchers import new_comment, new_vote, deleted_post
