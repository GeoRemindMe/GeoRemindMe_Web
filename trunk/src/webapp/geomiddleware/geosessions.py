import time
from django.utils.cache import patch_vary_headers
from django.conf import settings

from sessions.models import *

class geosession(object):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        if session_key is None:
            request.session = SessionStore.load(session_data=request.COOKIES.get(settings.SESSION_COOKIE_DATA_NAME, None))
        else:
            request.session = SessionStore.load(session_key=session_key)
            
    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            anonymous = request.session.anonymous
        except AttributeError:
            pass
        else:
            if anonymous:
                request.session.save()
                response.set_cookie(settings.SESSION_COOKIE_DATA_NAME,
                        request.session.data, max_age=None,
                       expires=None, domain=settings.SESSION_COOKIE_DOMAIN,
                       path=settings.SESSION_COOKIE_PATH,
                       secure=settings.SESSION_COOKIE_SECURE or None,
                      httponly=settings.SESSION_COOKIE_HTTPONLY or None)
                
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires = request.session.get_expires()
                # Save the session data and refresh the client cookie.
                request.session.save()
                response.set_cookie(settings.SESSION_COOKIE_NAME,
                        request.session.session_key, max_age=max_age,
                       expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                       path=settings.SESSION_COOKIE_PATH,
                       secure=settings.SESSION_COOKIE_SECURE or None,
                      httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response