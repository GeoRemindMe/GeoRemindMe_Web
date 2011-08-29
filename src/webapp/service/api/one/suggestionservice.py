# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Suggestion, Suggestions, ClientId

class GetSuggestionRequest(messages.Message):
    query_id = messages.IntegerField(1)
    page = messages.IntegerField(2, default=1)
    

class GetSyncSuggestion(messages.Message):
    last_sync = messages.IntegerField(1)
    suggestions = messages.MessageField(Suggestion, 2, repeated=True)


class AddSyncSuggestion(messages.Message):
    suggestions = messages.MessageField(Suggestion, 2, repeated=True)
  

class SuggestionService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSuggestionRequest, Suggestions)
    def get_suggestions(self, request):
        from geouser.models import User
        user = User.objects.get_by_username('jneight')
        from time import mktime
        from geoalert.models import Suggestion as SuggestionModel
        suggestions = SuggestionModel.objects.get_by_user(user,
                                                     user,
                                                     request.page, 
                                                     request.query_id)
        response = []
        for a in suggestions[1]:
            t = Suggestion(
                           name = a.name,
                           description = a.description,
                           poi_lat = a.poi.poi.lat,
                           poi_lon = a.poi.poi.lon,
                           poi_id = a.poi.id,
                           places_reference = a.poi.google_places_reference,
                           modified = int(mktime(a.modified.utctimetuple())),
                           created = int(mktime(a.created.utctimetuple())),
                           lists = [l.id for l in a.lists],
                           id = a.id,
                         )
            response.append(t)
        return Suggestions(query_id=suggestions[0], suggestions=response)
    
    @remote.method(GetSyncSuggestion, Suggestions)
    def sync_suggestions(self, request):
        from geouser.models import User
        if len(request.suggestions) > 20:
            from protorpc.remote import ApplicationError
            raise ApplicationError("Too many suggestions")
        user = User.objects.get_by_username('jneight')
        from datetime import datetime
        from time import mktime
        if request.last_sync is None:
            request.last_sync = int(mktime(user.created.utctimetuple()))
        from geoalert.models import Suggestion as SuggestionModel
        from geoalert.models_poi import Place as PlaceModel
        from google.appengine.ext import db
        clients_ids = []
        suggestions_to_save = []
        for a in request.suggestions:
            id = a.get('id', None)
            if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
                old = SuggestionModel.objects.get_by_id_user(id, request.user)
                if not old:  # no existe en la BD, fue borrada.
                    continue
            poi = PlaceModel.get_or_insert(location = a.poi_id,
                                      google_places_reference=a.places_reference,
                                      user = request.user)
            s = SuggestionModel.update_or_insert(
                         id = id,
                         name = a.get('name', u''),
                         description = a.get('description', u''),
                         user = user,
                         poi = poi,
                         commit = False
                         )
            suggestions_to_save.append(s) # juntamos para hacer un solo put
            clients_ids.append(a.client_id) # la alerta no estaba sincronizada
        db.put(suggestions_to_save)
        suggestions = SuggestionModel.objects.get_by_last_sync(user,
                                                     datetime.fromtimestamp(request.last_sync)
                                                     )
        response = [Suggestion(
                           name = a.name,
                           description = a.description,
                           poi_lat = a.poi.location.lat,
                           poi_lon = a.poi.location.lon,
                           poi_id = a.poi.id,
                           places_reference = a.poi.google_places_reference,
                           modified = int(mktime(a.modified.utctimetuple())),
                           created = int(mktime(a.created.utctimetuple())),
                           id = a.id,
                         ) for a in suggestions]
        for a, b in zip(response, clients_ids):
            if b is not None:
                response.client_id = b
        return Suggestions(suggestions=response)