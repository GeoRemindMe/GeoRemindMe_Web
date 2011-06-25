# coding=utf-8

import libs.oauth2 as oauth2
from google.appengine.ext import db

from models import OAUTH_Client, OAUTH_Token
from exceptions import *

"""
.. module:: backend
    :platform: appengine
    :synopsis: Backend functions
"""

class OAUTH_Store(object):
    """ Handle the models in the datastore (clients, tokens, etc)"""
    
    def fetch_consumer(self, oauth_request):
        """Load the consumer (key, secret) who is doing a request
        
                :param oauth_request: oauth request
                :type oauth_request: :class:`oauth2.Request`
                
                :retuns: :class:`oauth2.Consumer`
                :raises: :class:`OAUTHException` if the client key is invalid
        """
        key = oauth_request.get_parameter('oauth_consumer_key')
        if key is not None:
            client = OAUTH_Client.get_by_key_name(key)
            if client is None:
                raise OAUTHException("Client key invalid")
            return oauth2.Consumer(client.client_key, client.client_secret)
        return key
    
    
    def fetch_appInfo(self, key):
        """Returns a dict with the name and description of a client application
            
                :param key: App key in the datastore
                :type key: :class:`string`
                
                :returns: dict with the info of the app
                :raises: :class:`OAUTHException` if token key is invalid
        """
            
        token = OAUTH_Token.get_by_key_name(key)
        if token is not None:
            app = token.oauth_consumer
            return {'name' : app.name,
                    'description' : app.description,
                    }
        raise OAUTHException("Token key invalid")
    
    
    def generate_request_token(self, oauth_request, oauth_consumer, oauth_callback=None):
        """Load the request token in the request
        
                :param oauth_request: oauth request
                :type oauth_request: :class:`oauth2.Request`
                :param oauth_consumer: oauth consumer
                :type oauth_consumer: :class:`oauth2.Consumer`
                :param oauth_callback: callback URL
                :type oauth_callback: :class:`string`
                
                :returns: :class:`oauth2.Token` with the new key and secret
                :raises: :class:`OAUTHException` if client key is invalid
        """
        client = OAUTH_Client.get_by_key_name(oauth_consumer.key)
        if client is not None:
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
        raise OAUTHException("Client key invalid") 
    

    def authorize_token(self, token, user):
        """Authorizes a request token, sets the verifier and the user in the token
        
            :param token: Request token to be authorized
            :type token: :class:`oauth2.Token`
            :param user: User who authorizes the token
            :type user: :class:`georemindme.models.User`
            
            :returns: :class:`oauth2.Token` authorized
            :raises: :class:`OAUTHException` if the token key is invalid
        """
        authorizeToken = OAUTH_Token.get_by_key_name(token.key)
        if authorizeToken is not None:
            authorizeToken.authorize_token(user)
            token.set_verifier(authorizeToken.token_verifier)
            if authorizeToken.token_callback is not None:
                token.set_callback(authorizeToken.callback)
            return token
        raise OAUTHException("Token key invalid")
    
    
    def generate_access_token(self, token, oauth_consumer):
        """Generate the new access token
            
                :param token: Request token authorized
                :type token: :class:`oauth2.Token`
                :param oauth_consumer: Application requesting the access token
                :type oauth_consumer: :class:`oauth2.Consumer`
                :param user: User for the authorized token
                :type user: :class:`georemindme.models.User`
                
                :returns: :class:`oauth2.Token`
                :raises: :class:`OAUTHException` if the token key or consumer key are invalid
        """
        if token.verifier is None:
            raise OAUTHException('Unauthorized token')
        savedtoken = OAUTH_Token.get_by_key_name(token.key)        
        client = OAUTH_Client.get_by_key_name(oauth_consumer.key)
        if savedtoken is not None and client is not None:
            if token.verifier != savedtoken.token_verifier:
                raise OAUTHException("Token verifier invalid")
            accessToken = OAUTH_Token.generate(
                        oauth_consumer = client, 
                        oauth_user = savedtoken.oauth_user,
                        access = True
                        )
            savedtoken.delete() 
            oauthToken = oauth2.Token(accessToken.token_key, accessToken.token_secret)
            return oauthToken
        raise OAUTHException("Token or client key invalid")
    
    def fetch_token(self, oauth_request):
        """Get the token object in a request
        
                :param oauth_request: oauth request
                :type oauth_request: :class:`oauth2.Request`
                
                :returns: :class:`oauth2.Token`
                :raises: :class:`OAUTHException` if token is invalid
        """
        token = oauth_request.get_parameter('oauth_token')
        token = OAUTH_Token.get_by_key_name(token)
        if token is not None:
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
            if token.token_callback is not None:
                oauthToken.set_callback(token.token_callback)
            if token.token_verifier is not None:
                verifier = oauth_request.get_parameter('oauth_verifier')
                if verifier != token.token_verifier:
                    raise OAUTHException("Token key invalid") 
                oauthToken.set_verifier(token.token_verifier)
            return oauthToken
        raise OAUTHException("Token key invalid")
    
    def fetch_token_db(self, oauth_request):
        """Get the token object in a request
        
                :param oauth_request: oauth request
                :type oauth_request: :class:`oauth2.Request`
                
                :returns: :class:`oauth2.Token` and :class:`geoauth.models.OAUTH_Access`
                :raises: :class:`OAUTHException` if token is invalid
        """
        token = oauth_request.get_parameter('oauth_token')
        token = OAUTH_Token.get_by_key_name(token)
        if token is not None:
            oauthToken = oauth2.Token(token.token_key, token.token_secret)
            if token.token_callback is not None:
                oauthToken.set_callback(token.token_callback)
            if token.token_verifier is not None:
                verifier = oauth_request.get_parameter('oauth_verifier')
                if verifier != token.token_verifier:
                    raise OAUTHException("Token key invalid") 
                oauthToken.set_verifier(token.token_verifier)
            return oauthToken, token
        raise OAUTHException("Token key invalid") 
        
