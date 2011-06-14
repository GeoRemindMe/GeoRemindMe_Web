import time
from django.utils.cache import patch_vary_headers
from django.conf import settings

from sessions.store import *
from geouser.models import AnonymousUser

class geosession(object):
    def process_request(self, request):
        session_id = request.COOKIES.get(settings.COOKIE_NAME, None)
        """
        #  sesiones hibridas (usuarios en BD y anonimos en cookies
        if session_key is None:
            request.session = SessionStore.load(session_data=request.COOKIES.get(settings.SESSION_COOKIE_DATA_NAME, None))
        else:
        """
        if session_id is None:
            session_id = request.META.get('HTTP_X_GEOREMINDME_SESSION', None)
            request.session = SessionStore.load(session_id=session_id, from_cookie=False, from_rpc=True)
        """
        if session_key is None:
            # validar request
            # asignar usuario a request
            request.
        """
        if session_id is None:
            request.session = SessionStore.load(session_data=request.COOKIES.get(
                                             settings.COOKIE_DATA_NAME, None),
                                             from_cookie=False
                                             )
        else:
            request.session = SessionStore.load(session_id=session_id)
        
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
            except AttributeError:
                pass
            else:
                if anonymous:
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
                        if request.session.cookie_saved():
                            max_age = request.session.get_expiry_age()
                            expires = request.session.get_expires()
                        else:
                            max_age = None
                            expires = None# Save the session data and refresh the client cookie.
                        request.session.put()
                        response.set_cookie(settings.COOKIE_NAME,
		                                 request.session.session_id, max_age=max_age,
                                         expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                         path=settings.SESSION_COOKIE_PATH,
                                         secure=settings.SESSION_COOKIE_SECURE,
                                         #httponly=settings.COOKIE_SESSION_HTTPONLY or None
                                         )
        return response

