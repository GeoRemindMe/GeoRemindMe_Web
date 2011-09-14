# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Sites, Site

class GetSiteReverseRequest(messages.Message):
    name = messages.StringField(1)
    lat = messages.FloatField(2)
    lon = messages.FloatField(3)
    

class MapService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSiteReverseRequest, Sites)
    def get(self, request):
        if request.name is not None and len(request.name) < 3:
            from protorpc.remote import ApplicationError
            raise ApplicationError("Name too small")
        from google.appengine.ext.db import GeoPt
        poi = GeoPt(request.lat, request.lon)
        from libs.httplib2 import Http
        import memcache
        mem = memcache.mem.Client()
        r = Http(cache=mem)
        if request.name is not None:
            from urllib import quote_plus
            name = quote_plus(request.name.strip())
            url = 'http://andaluciapeople.com/granada/sitios.json/lat/%s/lng/%s/?q=%s' % (poi.lat, poi.lon, name)
        else:
            url = 'http://andaluciapeople.com/granada/sitios.json/lat/%s/lng/%s/' % (poi.lat, poi.lon)
        response, content = r.request(url,
                                      method='GET',
                                      headers={ 'User-Agent' : 'Georemindme:0.1' }
                                     )
#        from mapsServices.places.GPRequest import GPRequest
#        google_places = GPRequest()
#        results = google_places.do_search(pos=poi, name=request.name)
#        response = [Site(name=r['name'], 
#                       lat=r['geometry']['location']['lat'], 
#                       lon=r['geometry']['location']['lng'],
#                       address=r.get('formatted_address')
#                       ) for r in results['results'][0:8]
#                  ]
        if response['status'] != 200:
            from protorpc.remote import ApplicationError
            raise ApplicationError("Error in request")
        from django.utils import simplejson
        json = simplejson.loads(content)
        results = [Site(name=r['nombre'], 
                       lat=r['lat'], 
                       lon=r['lng'],
                       ) for r in json[:7]
                  ]
        return Sites(sites=results)
