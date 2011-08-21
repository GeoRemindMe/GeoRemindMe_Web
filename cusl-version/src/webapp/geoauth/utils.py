# coding=utf-8
import oauth2

from exceptions import OAUTHException
from models import OAUTH_Client

def validate_client(request):
    """Validate a client doing the oauth request
            
            :param Request: A valid request
            :type Request: :class:`Request`
            :return: :class:`OAUTH_Client`
            :raises: :class:`OAUTHException
    """
    
    def _get_oauth_request(request):
        """Return an OAuth Request object for the current request.
        
            :param Request: A valid request
            :type Request: :class:`Request`
            :return: :class:`oauth2.Request`
        """
        return oauth2.Request.from_request(request.method, request.build_absolute_uri(),
            headers=request.META, query_string=request.raw_post_data)
        
    def _get_client(oauthRequest):
        """Return the client doing the oauth request
        
            :param oauthRequest: A valid oauth request
            :type oauthRequest: :class:`oauth2.Request`
            :return: :class:`OAUTH_Client
            :raises: :class:`OAUTHException`
        """
        if not isinstance(oauthRequest, oauth2.Request):
            oauthRequest = _get_oauth_request(oauthRequest)
        client_key = oauthRequest.get_parameters('oauth_consumer_key')
        if not client_key:#la peticion oauth no es valida
            raise OAUTHException("No 'oauth_consumer_key' in request")
        client = OAUTH_Client.get_by_key_name(client_key)
        if not client:#el usuario no existe
            raise OAUTHException("Invalid client in request")
        return client
        
    def is_valid(request):
        """Return the valid client or raise a Exception
            
            :param Request: A valid request
            :type Request: :class:`Request`
            :return: :class:`OAUTH_Client`
            :raises: :class:`OAUTHException
        """
        try:
            client = _get_client(request)
            #comprueba que la firma sea correcta
            server = oauth2.Server()
            server.add_signature_method(oauth2.SignatureMethod_HMAC_SHA1())
            server.add_signature_method(oauth2.SignatureMethod_PLAINTEXT())
            params = server.verify_request(request, client, None)
        except Exception, e:
            raise e
        return client
    return is_valid(request)