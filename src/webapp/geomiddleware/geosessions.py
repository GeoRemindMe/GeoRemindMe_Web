import time
from django.utils.cache import patch_vary_headers
from django.conf import settings

from sessions.store import SessionStore
from geouser.models import AnonymousUser

class geosession(object):
    def process_request(self, request):
        session_id = request.COOKIES.get(settings.COOKIE_NAME, None)
        if session_id is None:
            session_id = request.META.get('HTTP_X_GEOREMINDME_SESSION', None)
            request.session = SessionStore.load(session_id=session_id, from_cookie=False, from_rpc=True)
        if session_id is None:
            request.session = SessionStore.load(session_data=request.COOKIES.get(
                                             settings.COOKIE_DATA_NAME, None),
                                             from_cookie=False
                                             )
        else:
            request.session = SessionStore.load(session_id=session_id)
        
        if hasattr(request, 'facebook'):
            if request.facebook['client'].user is not None:                
                if not 'user' in request.session:
                    from facebookApp import watchers   
                    request.session.delete()
                    request.session.init_session(user=request.facebook['client'].user, is_from_facebook=True)
                    request.user = request.session['user']
                    return
                # sesion iniciada en web y facebook
                else:
                    if request.session['user'].id != request.facebook['client'].user.id:
#                        from facebookApp import watchers
#                        request.session.delete()
#                        request.session = SessionStore.init_session(user=request.facebook['client'].user)
#                        request.user = request.session['user']
#                        return
                        from django.shortcuts import render_to_response
                        from django.template import RequestContext
                        user_logged = request.session['user']
                        request.session.delete()
                        request.user = AnonymousUser()
                        
                        return render_to_response('login_problem.html', 
                                              {'user_logged': user_logged,
                                               'user_fb': request.facebook['client'].user,
                                               },
                                              context_instance=RequestContext(request)
                                              )
        else:
            if request.session.is_from_facebook:
                request.session.delete()
                request.user = AnonymousUser()
                from facebookApp.watchers import disconnect_all
                disconnect_all()
                return
        if 'user' in request.session:
            request.user = request.session['user']
        else:
            request.user = AnonymousUser()

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        if hasattr(request, 'session'):
            try:
                accessed = request.session._accessed
                modified = request.session._modified
                anonymous = request.session._anonymous
                cookieless = request.session._cookieless
                deleted = request.session._deleted
            except AttributeError:
                pass
            else:
                if deleted:
                    response.delete_cookie(settings.COOKIE_NAME, path=settings.SESSION_COOKIE_PATH, domain=settings.SESSION_COOKIE_DOMAIN)
                    response.delete_cookie('fbs_%s' % settings.OAUTH['facebook']['app_key'], path=settings.SESSION_COOKIE_PATH, domain=settings.SESSION_COOKIE_DOMAIN)
                elif cookieless:
                    request.session.put()
                elif anonymous:
                    response.set_cookie(settings.COOKIE_DATA_NAME,
                                        request.session.data, max_age=None,
                                        expires=None, domain=settings.COOKIE_DOMAIN,
                                        path=settings.COOKIE_PATH,
                                        secure=False,
                                        #httponly=settings.COOKIE_SESSION_HTTPONLY or None
                                        )
                else:
                    if accessed:
                        patch_vary_headers(response, ('Cookie',))
                    if modified:
                        max_age = None
                        expires = None
                        if request.session.cookie_saved():
                            max_age = request.session.get_expiry_age()
                            expires = request.session.get_expires()
                        request.session.put()
                        response.set_cookie(settings.COOKIE_NAME,
		                                 request.session.session_id, max_age=max_age,
                                         expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                         path=settings.SESSION_COOKIE_PATH,
                                         secure=settings.SESSION_COOKIE_SECURE,
                                         #httponly=settings.COOKIE_SESSION_HTTPONLY or None
                                         )
        return response

