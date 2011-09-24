# coding=utf-8

""" Fusion Tables Client.

Issue requests to Fusion Tables.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'
__maintainer__ = "javier@georemindme.com (Javier Cordero)"

import libs.httplib2 as httplib2
import libs.oauth2 as oauth2
import urllib


class FTAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type

        
class FTClient():
    def _get(self, query): pass
    def _post(self, query): pass
    
    def query(self, query, request_type=None):
        """ Issue a query to the Fusion Tables API and return the result. """
        
        #encode to UTF-8
        try: query = query.encode("utf-8")
        except: query = query.decode('raw_unicode_escape').encode("utf-8")
        
        lowercase_query = query.lower()
        if lowercase_query.startswith("select") or \
           lowercase_query.startswith("describe") or \
           lowercase_query.startswith("show") or \
           request_type=="GET":
        
            return self._get(urllib.urlencode({'sql': query}))
        
        else:
            return self._post(urllib.urlencode({'sql': query}))

    
class OAuthFTClient(FTClient):

    def __init__(self):
        from django.conf import settings
        self.consumer_key = settings.OAUTH['google']['app_key']
        self.consumer_secret = settings.OAUTH['google']['app_secret']
        self.token = oauth2.Token(settings.FUSIONTABLES['token_key'], settings.FUSIONTABLES['token_secret'])
        self.scope = "https://www.google.com/fusiontables/api/query"

    def _get(self, query):
        consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
        client = oauth2.Client(consumer, self.token)
        resp, content = client.request(uri="%s?%s" % (self.scope, query),
                                        method="GET")
        return content


    def _post(self, query):
        consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)
        client = oauth2.Client(consumer, self.token)
        resp, content = client.request(uri=self.scope,
                                       method="POST",
                                       body=query)
        if resp['status'] != 200:
            raise Exception(content)
        return content
