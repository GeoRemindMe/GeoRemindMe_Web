# coding=utf-8

class OAuthware(object):
    def __init__(self, app):
        self.wrapped_app = app
        
    def __call__(self, environ, start_response):
        if 'HTTP_X_CSRFTOKEN' in environ: 
            import Cookie
            csrf_cookie = csrf_cookie = Cookie.SimpleCookie(environ.get("HTTP_COOKIE","")).get("csrftoken", None)
            if environ['HTTP_X_CSRFTOKEN'] != '' and csrf_cookie is not None:
                def _sanitize_token(token):
                    # from https://code.djangoproject.com/browser/django/trunk/django/middleware/csrf.py
                    import re
                    token = re.sub('[^a-zA-Z0-9]', '', str(token.decode('ascii', 'ignore')))
                    return token
                csrf_token = _sanitize_token(environ['HTTP_X_CSRFTOKEN'])
                csrf_cookie = _sanitize_token(csrf_cookie.value)
                if csrf_token == csrf_cookie:
                    return self.wrapped_app(environ, start_response)
                else:
                    start_response(403, [('content-type', 'text/plain')])
                    return ('Access forbidden') 
        return self.wrapped_app(environ, start_response)
