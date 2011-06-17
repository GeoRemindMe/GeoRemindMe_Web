# coding=utf-8
"""
.. module:: OAUTH_Server
    :platform: appengine
    :synopsis: OAUTH Server
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""

import lib.oauth2 as oauth2
from backend import OAUTH_Store
from exceptions import *

class OAUTH_Server(oauth2.Server):
    """Handles all the oauth requests"""
    
    def __init__(self, *args, **kwargs): 
        super(self.__class__, self).__init__(*args, **kwargs)
        self.add_signature_method(oauth2.SignatureMethod_PLAINTEXT())
        self.add_signature_method(oauth2.SignatureMethod_HMAC_SHA1())
        self.backend = OAUTH_Store()
        
        
    def _get_oauth_request(self, request):
        """Return an OAuth Request object for the current request.
        
            :param Request: A valid request
            :type Request: :class:`http.Request`
            :return: :class:`oauth2.Request`
        """
        return oauth2.Request.from_request(request.method, request.build_absolute_uri(),
            headers=request.META, query_string=request.raw_post_data)
        
        
    def token_requested(self, request):
        """The server generates a new token request for a consumer
        
            :param request: A valid request
            :type request: :class:`http.Request`
            :return: :class:`oauth2.Token`
        """
        oauthRequest = self._get_oauth_request(request)
        oauthConsumer = self.backend.fetch_consumer(oauthRequest)
        self.verify_request(oauthRequest, oauthConsumer, None)
        try:
            callback = oauthRequest.get_parameter('oauth_callback')
            return self.backend.generate_request_token(oauthRequest, oauthConsumer, callback)
        except:
            return self.backend.generate_request_token(oauthRequest, oauthConsumer, None)
    
    
    def appInfo_requested(self, token):
        """Returns a dict with the application info
            
            :param token: A token key
            :type token: :class:`string`
            :return: :class:`dict`
        """
        return self.backend.fetch_appInfo(token)
    
        
    def authorization_token_requested(self, request, user):
        """The user has accepted the application
        
            :param Request: A valid request
            :type Request: :class:`http.Request`
            :param user: The user who authorizes
            :type user: :class:`georemindme.models.User`
            :return: :class:`oauth2.Token`
        """
        oauthRequest = self._get_oauth_request(request)
        oauthToken = self.backend.fetch_token(oauthRequest)
        oauthToken = self.backend.authorize_token(oauthToken, user)
        
        return oauthToken
    
    
    def access_token_requested(self, request):
        """Return the access token from a authorized token
        
            :param Request: A valid request
            :type Request: :class:`http.Request`
            :param user: The user who authorizes
            :type user: :class:`georemindme.models.User`
            :return: :class:`oauth2.Token`
        """
        oauthRequest = self._get_oauth_request(request)
        oauthConsumer = self.backend.fetch_consumer(oauthRequest)
        oauthToken = self.backend.fetch_token(oauthRequest)
        self.verify_request(oauthRequest, oauthConsumer, oauthToken)
        accessToken = self.backend.generate_access_token(oauthToken, oauthConsumer)
        return accessToken

    def access_token_authentication(self, request):
        """Returns the user from a valid access token
        
            :param request: A valid request
            :type request: :class:`http.Request`
            
            :returns: :class:`geouser.models.User`
            :raises: :class:`OAUTHException` :class:`Error`
        """
        oauthRequest = self._get_oauth_request(request)
        oauthConsumer = self.backend.fetch_consumer(oauthRequest)
        oauthToken, datastoreToken = self.backend.fetch_token_db(request)
        self.verify_request(oauthRequest, oauthConsumer, oauthToken)
        if datastoreToken.access:
            return datastoreToken.user
        raise OAUTHException('Invalid token')