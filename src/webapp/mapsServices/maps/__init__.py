#coding=utf-8


from libs.httplib2 import Http
from google.appengine.ext import db
import memcache
import json as simplejson


class MapsAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type


class MapsRequest(Http):
    _reverse_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
    headers = { 'User-Agent' : 'Georemindme:0.1' }
    
    def __init__(self, *args, **kwargs):
        mem = memcache.mem.Client()
        super(self.__class__, self).__init__(cache=mem, *args, **kwargs)
        
        
    def get_address(self, location, sensor=False):
        if not isinstance(location, db.GeoPt):
            return MapsAPIError('invalid location')
        url = self._reverse_url + 'latlng=%f,%f&sensor=%s' % (location.lat, 
                                                    location.lon, 
                                                    ('true' if sensor else 'false')
                                                    )
        return self._do_request(url)
        
    def _do_request(self, url, method='GET', body=None):
        """
            Realiza una peticion por GET a la direccion recibida
            
                :param url: direccion url a donde hacer la peticion
                :type url: string
                
                :returns: diccionario con el resultado
                :raises: :class:`GPAPIError`
        """
        response, content = self.request(url, method=method, body=body, headers=self.headers)
        if int(response['status']) != 200:
            raise MapsAPIError(response['status'], content)
        json = simplejson.loads(content)
        return json 