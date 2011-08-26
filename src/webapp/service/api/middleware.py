# coding=utf-8

class OAuthware(object):
    def __init__(self, app):
        self.wrapped_app = app
        
    def __call__(self, environ, start_response):
        import libs.oauth2 as oauth2
        if 'HTTP_X_GEOREMINDME_SESSION' in environ:
            session_id = environ['HTTP_X_GEOREMINDME_SESSION']
            from geomiddleware.sessions.store import SessionStore
            session = SessionStore.load(session_id=session_id, from_cookie=False, from_rpc=True)
            if session is not None:
                environ['user'] = session.user
                session.put()
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
                    environ['user'] = token.user
                    return self.app(environ, start_response)
        start_response('403 ACCESS FORBIDDEN', [('content-type', 'text/plain')])
        return ('Access forbidden')
