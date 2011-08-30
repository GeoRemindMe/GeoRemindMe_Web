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
        from mapsServices.places.GPRequest import GPRequest
        google_places = GPRequest()
        results = google_places.do_search(pos=poi, name=request.name)
        response = [Site(name=r['name'], 
                       lat=r['geometry']['location']['lat'], 
                       lon=r['geometry']['location']['lng'],
                       address=r.get('formatted_address')
                       ) for r in results['results']
                  ]
        return Sites(sites=response)