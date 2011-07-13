import time
from django.utils.cache import patch_vary_headers
from django.conf import settings

from sessions.store import *
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

        if 'user' in request.session:
            request.user = request.session['user']
            if request.session.is_from_facebook and not hasattr(request, 'facebook'):
                request.session.delete()
                request.user = AnonymousUser()
            elif hasattr(request, 'facebook'):
                fbuser = request.user.facebook_user
                if fbuser is None:
                    if request.facebook['client'].user is not None:
                        delattr(request, 'facebook')
                        request.session.delete()
                        request.user = AnonymousUser()
                else:
                    if request.facebook['uid'] != fbuser.uid:
                        delattr(request, 'facebook')
                        request.session.delete()  
                        request.user = AnonymousUser()
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
        
        #if hasattr(request, 'facebook'):
            #response.delete_cookie("fbs_" + settings.OAUTH['facebook']['app_key'])
        return response

