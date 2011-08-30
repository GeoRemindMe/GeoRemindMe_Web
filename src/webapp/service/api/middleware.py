# coding=utf-8

class OAuthware(object):
    def __init__(self, app):
        self.wrapped_app = app
        
    def __call__(self, environ, start_response):
        import os
        return self.wrapped_app(environ, start_response)
        import libs.oauth2 as oauth2
        if 'HTTP_X_GEOREMINDME_SESSION' in environ:
            session_id = environ['HTTP_X_GEOREMINDME_SESSION']
            from geomiddleware.sessions.store import SessionStore
            session = SessionStore.load(session_id=session_id, from_cookie=False, from_rpc=True)
            if session is not None:
                os.environ['user'] = session.user
                session.put()
                return self.wrapped_app(environ, start_response)
        elif 'HTTP_AUTHORIZATION' in environ:
            headers = {'Authorization': environ['HTTP_AUTHORIZATION']}
            oauth_request = oauth2.Request.from_request(http_method=environ['REQUEST_METHOD'],
                                        http_url=environ['PATH_INFO'], 
                                        headers=headers,
                                        )
            if oauth_request is not None:
                from geoauth.models import OAUTH_Token
                token = OAUTH_Token.get_token(oauth_request.parameters['oauth_token'])
                if token.access:
                    os.environ['user'] = token.user
                    return self.wrapped_app(environ, start_response)
        elif environ['REQUEST_METHOD'] == 'POST':
            import Cookie
            csrf_cookie = Cookie.SimpleCookie(environ.get("HTTP_COOKIE","")).get("csrftoken", None)
            if csrf_cookie is not None:
                def _sanitize_token(token):
                    # from https://code.djangoproject.com/browser/django/trunk/django/middleware/csrf.py
                    import re
                    token = re.sub('[^a-zA-Z0-9]', '', str(token.decode('ascii', 'ignore')))
                    return token
                csrf_cookie = csrf_cookie.value
                csrf_token = _sanitize_token(csrf_cookie)
                post_env = environ.copy()
                a = post_env['wsgi.input'].read()
                #csrfmiddlewaretoken
                if csrf_token in a:
                    return self.wrapped_app(environ, start_response)
        start_response('403 ACCESS FORBIDDEN', [('content-type', 'text/plain')])
        return ('Access forbidden')
