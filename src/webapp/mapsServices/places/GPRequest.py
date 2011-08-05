# coding=utf-8

from libs.httplib2 import Http
from xml.etree import ElementTree

from django.conf import settings
from django.utils import simplejson

from google.appengine.api.memcache import Client

from geoalert.models_poi import Place


class GPAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type

class GPRequest(Http):
    '''
        encapsulates the queries
    '''
    _search_url = 'https://maps.googleapis.com/maps/api/place/search/json?'
    _details_url = 'https://maps.googleapis.com/maps/api/place/details/json?'
    _checkin_url = 'https://maps.googleapis.com/maps/api/place/check-in/json?'
    headers = { 'User-Agent' : 'Georemindme:0.1' }

    
    def __init__(self, *args, **kwargs):
        mem = Client()
        super(self.__class__, self).__init__(cache=mem, timeout=20, *args, **kwargs)
        self.key = settings.API['google_places']

    
    def do_search(self, pos, radius=500, types=None, language=None, name=None, sensor=False):
        """
            Realiza una busqueda en Google Places. Añade '_url' a cada resultado con la direccion para acceder
            a nuestra informacion del sitio. Si commit es True, los resultados con ids que no existan en la BD
            seran añadidos
            
                :param pos: posicion a buscar
                :type pos: :class:`db.GeoPt`
                :param radius: radio para hacer las busquedas
                :type radius: integer
                :param types: tipos de lugares a buscar
                :type types: list
                :param language: idioma para mostrar los resultados
                :type language: string
                :param name: nombre del lugar a buscar
                :type name: string
                :param sensor: indicar si la posicion se obtiene con algun sensor (GPS, ...)
                :type sensor: boolean
                :param commit: Indicar si se debe añadir los resultados que no existan a la BD
                :type commit: boolean
                
                :returns: diccionario con los resultados
                :raises: :class:`GPAPIError`
        """                
        url = self._search_url + 'location=%s,%s&radius=%s' % (pos.lat, pos.lon, radius)
        if types is not None:
            if type(types) != type(list()):
                types = list(types)
            types = '|'.join(types)
            url = url + '&types=%s' % types
        if language is not None:
            url = url + '&language=%s' % language
        if name is not None:
            url = url + '&name=%s' % name
        url = url + '&sensor=%s&key=%s' % ('true' if sensor else 'false', self.key)
        return self._do_request(url)
    
        
    def retrieve_reference(self, reference, language=None, sensor=False):
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
        url = self._details_url + 'reference=%s' % reference
        if language is not None:
            url = url + '&language=%s' % language
        url = url + '&sensor=%s&key=%s' % ('true' if sensor else 'false', self.key)
        return self._do_request(url)
    
    
    def do_checkin(self, reference, sensor = True):
        url = self._checkin_url + 'sensor=%s&key=%s' % ('true' if sensor else 'false', self.key)
        return self._do_request(url, method='POST', body='reference: %s' % reference)
    
    def add_place(self):
        pass
        
    def _do_request(self, url, method='GET', body=None):
        """
            Realiza una peticion por GET a la direccion recibida
            
                :param url: direccion url a donde hacer la peticion
                :type url: string
                
                :returns: diccionario con el resultado
                :raises: :class:`GPAPIError`
        """
        response, content = self.request(url, method=method, body=body, headers=self.headers)
        if response['status'] != 200:
            raise GPAPIError(response['status'], 'ERROR IN REQUEST')
        json = simplejson.loads(content)
        if json['status'] == 'OK':
            return json
        raise GPAPIError(json['status'])