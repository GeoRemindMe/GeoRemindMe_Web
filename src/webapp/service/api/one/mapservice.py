# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages
from protorpc.remote import ApplicationError

from messages import Sites, Site, Place, Suggestions, Suggestion

class GetSiteReverseRequest(messages.Message):
    name = messages.StringField(1)
    lat = messages.FloatField(2)
    lon = messages.FloatField(3)
    

class GetPlaceRequest(messages.Message):
    """
            Parametros de entrada para realizar una peticion de informacion de
        un sitio.
            
            Parametros:
                id : :class:`Integer` codigo ID que identifica al lugar
                google_places_reference: :class:`string` codigo que identifica 
                    el lugar en google places
            
            Ambos parametros son opcionales, pero al menos debes indicar uno, 
        teniendo id, preferencia sobre google_places_reference
    """
    id = messages.IntegerField(1)
    google_places_reference = messages.StringField(2)
    

class MapService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSiteReverseRequest, Sites)
    def get(self, request):
        if request.name is not None and len(request.name) < 3:
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
            raise ApplicationError("Error in request")
        from django.utils import simplejson
        json = simplejson.loads(content)
        results = [Site(name=r['nombre'], 
                       lat=r['lat'], 
                       lon=r['lng'],
                       ) for r in json[:7]
                  ]
        return Sites(sites=results)
    
    
    @remote.method(GetPlaceRequest, Place)
    def get_place(self, request):
        """
                Devuelve la informacion sobre un determinado sitio, incluyendo
            la lista de sugerencias.
            
                Recibe :class:`GetPlaceRequest` con el lugar a buscar.
                
                Devuelve: :class:`Place` con la informacion del sitio y las sugerencias
                    existentes.
                    
                Excepciones: :class:`ApplicationError` si no existe o faltan parametros
                    para identificar el sitio.
        """
        from geouser.models import User
        from geoalert.models_poi import Place as PlaceModel
        from geovote.models import Vote
        from geoalert.models import Suggestion as SuggestionModel
        from geoalert.views import _get_city
        from os import environ
        from time import mktime
        from google.appengine.ext import db
        if request.id is None and request.google_places_reference is None:
            raise ApplicationError("Unknow place")
        user = User.objects.get_by_id(int(environ['user']))
        def load_suggestions_async(suggestions):
            suggestions_loaded = [s for s in suggestions]
            from georemindme.funcs import prefetch_refprops
            suggestions = prefetch_refprops([s for s in suggestions_loaded], SuggestionModel.user, SuggestionModel.poi)
            suggestions_loaded = []
            for a in suggestions:
                t = Suggestion(
                           name = a.name,
                           description = a.description,
                           poi_lat = a.poi.location.lat,
                           poi_lon = a.poi.location.lon,
                           poi_id = a.poi.id,
                           google_places_reference = a.poi.google_places_reference,
                           modified = int(mktime(a.modified.utctimetuple())),
                           created = int(mktime(a.created.utctimetuple())),
                           username = a.user.username,
                           id = a.id,
                         )
                suggestions_loaded.append(t)
            return suggestions_loaded
        if request.id is not None:
            place = PlaceModel.objects.get_by_id(request.id)
        else:
            place = PlaceModel.objects.get_by_google_reference(request.google_places_reference)
        if place is None:
            raise ApplicationError("Unknow place")
        query_id, suggestions_async = SuggestionModel.objects.get_by_place(place, 
                                                  querier=user,
                                                  async = True
                                                  )
        
        vote_counter = Vote.objects.get_vote_counter(place.key())
        # es un lugar cargado desde google places
        if place.google_places_reference is not None:
            from mapsServices.places.GPRequest import GPRequest
            try:    
                search = GPRequest().retrieve_reference(place.google_places_reference)
                place.update(name=search['result']['name'],
                            address=search['result'].get('formatted_address'), 
                            city=_get_city(search['result'].get('address_components')),
                            location=db.GeoPt(search['result']['geometry']['location']['lat'], search['result']['geometry']['location']['lng']),
                            google_places_reference=search['result']['reference'],
                            google_places_id=search['result']['id']
                            )
            except: 
                pass
        
        return Place(id = place.id,
                     name = place.name,
                     address = place.address,
                     city = place.city,
                     poi_lat = place.location.lat,
                     poi_lon = place.location.lon,
                     suggestions = Suggestions(query_id= query_id,
                                               suggestions = load_suggestions_async(suggestions_async)
                                               ),
                     vote_counter = vote_counter,
                     google_places_reference=place.google_places_reference
                     )