# coding=utf-8

import oauth2
from google.appengine.ext import db

from models import OAUTH_Client, OAUTH_Token
from exceptions import *

class OAUTH_Store(object):
    """Handle the models in datastore (clients, token, etc.)"""
    def fetch_consumer(self, oauth_request):
        """Load the consumer (key, secret) doing a request
        
            :param oauth_request: oauth request
            :type oauth_request: :class:`oauth2.Request`
        """
        key = oauth_request.get_parameter('oauth_consumer_key')
        if key is not None:
            client = OAUTH_Client.get_by_key_name(key)
            if client is None:
                raise OAUTHException("Client key invalid")
            return oauth2.Consumer(client.client_key, client.client_secret)
        return key
    
    def fetch_appInfo(self, key):
        """Returns a dict with the name and description of a client application"""
        token = OAUTH_Token.get_by_key_name(key)
        if token is not None:
            app = token.oauth_consumer
            return {'name' : app.name,
                    'description' : app.description,
                    }
        raise OAUTHException("Token key invalid")
    
    def fetch_request_token(self, oauth_request, oauth_consumer, oauth_callback=None):
        """Load the token in the request
        
            :param oauth_request: oauth request
            :type oauth_request: :class:`oauth2.Request`
            :param oauth_consumer: oauth consumer
            :type oauth_consumer: :class:`oauth2.Consumer`
            :param oauth_callback: callback URL
            :type oauth_callback: :class:`string`
        """
        client = OAUTH_Client.get_by_key_name(oauth_consumer.key)
        """
        try:
            key = oauth_request.get_parameter('oauth_token')
        except:
            key = None
        #buscar el token en la BD
        if key is not None:
            token = self.fetch_token(oauth_request)
            if token.oauth_client.key != oauth_consumer.key:
                raise OAUTHException("Token key invalid")
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
            if oauth_callback is not None:
                token.token_callback(oauth_callback)
                token.put()
                oauthToken.set_callback(oauth_callback)
            elif client.callback is not None:
                token.token_callback(client.callback)
                token.put()
                oauthToken.set_callback(oauth_callback)              
        #el token no existe, crear uno nuevo
        """
        if oauth_callback is not None:
            token = OAUTH_Token.generate(oauth_consumer = client, token_callback=oauth_callback)
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
            oauthToken.set_callback(oauth_callback)
        elif client.callback is not None:
            token = OAUTH_Token.generate(oauth_consumer = client, token_callback=client.callback)
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
            oauthToken.set_callback(client.callback)
        else:
            token = OAUTH_Token.generate(oauth_consumer = client)
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
        return oauthToken
    
    def authorize_token(self, token, user):
        """Sets the verifier and the user in the token
        
            :param token: Request token to be authorized
            :type token: :class:`oauth2.Token`
            :param user: User for the authorized token
            :type user: :class:`georemindme.models.User`
        """
        
        authorizeToken = OAUTH_Token.get_by_key_name(token.key)
        authorizeToken.authorize_token(user)
        token.set_verifier(authorizeToken.token_verifier)
        if authorizeToken.token_callback is not None:
            token.set_callback(authorizeToken.callback)
        return token
    
    def fetch_access_token(self, token, oauth_consumer):
        """Generate the new access token
            
            :param token: Request token authorized
            :type token: :class:`oauth2.Token`
            :param oauth_consumer: Application requesting the access token
            :type oauth_consumer: :class:`oauth2.Consumer`
            :param user: User for the authorized token
            :type user: :class:`georemindme.models.User`
        """
        if token.verifier is None:
            raise OAUTHException('Unauthorized token')
        token = OAUTH_Token.get_by_key_name(token.key)        
        client = OAUTH_Client.get_by_key_name(oauth_consumer.key)
        #los token de acceso, tienen el mismo verifier
        accessToken = OAUTH_Token.generate(
                    oauth_consumer = client, 
                    oauth_user = token.oauth_user,
                    access = True
                    )
        token.delete()
        #el token a devolver
        oauthToken = oauth2.Token(accessToken.token_key, accessToken.token_secret)
        return oauthToken
    
    def fetch_token(self, oauth_request):
        """Get the token object in a request
        
            :param oauth_request: oauth request
            :type oauth_request: :class:`oauth2.Request`
        """
        token = oauth_request.get_parameter('oauth_token')
        token = OAUTH_Token.get_by_key_name(token)
        if token is None:
            raise OAUTHException("Token key invalid")            
        oauthToken = oauth2.Token(token.token_key, token.token_secret)
        if token.token_callback is not None:
            oauthToken.set_callback(token.token_callback)
        if token.token_verifier is not None:
            verifier = oauth_request.get_parameter('oauth_verifier')
            if verifier != token.token_verifier:
                raise OAUTHException("Token key invalid") 
            oauthToken.set_verifier(token.token_verifier)
        return oauthToken