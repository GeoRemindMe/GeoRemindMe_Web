# coding=utf-8

from libs.oauth2 import Consumer
from libs.httplib2 import Http
from google.appengine.api.memcache import Client


class FSAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type


class FSRequest(Http):
    _details_url = 'https://api.foursquare.com/v2/venues/'
    headers = { 'User-Agent' : 'Georemindme:0.1', 'Accept-Language': 'en' }
    
    def __init__(self, *args, **kwargs):
        from django.conf import settings
        mem = Client()
        super(self.__class__, self).__init__(cache=mem, timeout=20, *args, **kwargs)
        self.consumer = Consumer(settings.OAUTH['foursquare']['app_key'], 
                                 settings.OAUTH['foursquare']['app_secret']
                                 )
        
    def retrieve_reference(self, venueid, language=None, sensor=False):
        """
            Realiza una busqueda en Google Places de un lugar concreto. Añade '_url'
            al resultado con nuestra url al lugar
            
                :param pos: posicion a buscar
                :type pos: :class:`db.GeoPt`
                :param language: idioma para mostrar los resultados
                :type language: string
                :param sensor: indicar si la posicion se obtiene con algun sensor (GPS, ...)
                :type sensor: boolean
                
                :returns: diccionario con los resultados
                :raises: :class:`GPAPIError`
        """ 
        url = self._details_url + venueid
        return self._do_request(url, language=language)
    
    def _do_request(self, url, method='GET', body=None, language=None):
        """
            Realiza una peticion por GET a la direccion recibida
            
                :param url: direccion url a donde hacer la peticion
                :type url: string
                :param method: Metodo para enviar los parametros
                :type method: string
                :param body: datos para enviar en peticion POST
                :type body: string
                
                :returns: diccionario con el resultado
                :raises: :class:`GPAPIError`
        """
        try:
            import json as simplejson
        except:
            from django.utils import simplejson
        if language is not None:
            self.headers['Accept-Language'] = language
        response, content = self.request(url, method=method, body=body, headers=self.headers)
        json = simplejson.loads(content)
        if response['status'] == 200:
            if json['meta']['code'] == '200':
                return json
        raise FSAPIError(json['meta']['errorType'], json['meta']['errorDetail'])
    
    