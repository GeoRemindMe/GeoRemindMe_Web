# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Suggestion, Suggestions, List

from time import mktime
from os import environ


from geoalert.api import get_suggestions_dict
from geoalert.models import Suggestion as SuggestionModel
from geouser.models import User
from geolist.models import ListSuggestion
from geovote.models import Vote, Comment
from google.appengine.ext import db
from georemindme.funcs import prefetch_refprops, prefetch_refList, single_prefetch_refprops

class GetSuggestionsRequest(messages.Message):
    query_id = messages.IntegerField(1)
    page = messages.IntegerField(2, default=1)
    

class GetSuggestionRequest(messages.Message):
    id = messages.IntegerField(1, required=True)
    

#class GetSyncSuggestion(messages.Message):
#    last_sync = messages.IntegerField(1)
#    suggestions = messages.MessageField(Suggestion, 2, repeated=True)
#
#
#class AddSyncSuggestion(messages.Message):
#    suggestions = messages.MessageField(Suggestion, 2, repeated=True)
  

class SuggestionService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSuggestionsRequest, Suggestions)
    def get_suggestions(self, request):
        user = User.objects.get_by_id(int(environ['user']))
        lists_following = ListSuggestion.objects.get_list_user_following(user, async=True)
        lists = ListSuggestion.objects.get_by_user(user=user, querier=user, all=True)
        suggestions_entity = get_suggestions_dict(user) 
        suggestions = []
        for s in suggestions_entity: # convertir entidades
            sug = db.model_from_protobuf(s.ToPb())
            setattr(sug, 'lists', [])
            suggestions.append(sug)
        suggestions = prefetch_refprops(suggestions, SuggestionModel.user, SuggestionModel.poi)
        # combinar listas
        lists = [l for l in lists]
        lists.extend(ListSuggestion.objects.load_list_user_following_by_async(lists_following, resolve=True))
        # construir un diccionario con todas las keys resueltas y usuarios
        #instances = prefetch_refList(lists, users=[ListSuggestion.user.get_value_for_datastore(l) for l in lists])
        lists = [l.to_dict(resolve=False) for l in lists]
        # añadimos las listas
        #[s.lists.append(l) for l in lists for s in suggestions if s.id in l['keys']]
        response = []
        for a in suggestions:
            t = Suggestion(
                           name = a.name,
                           description = a.description,
                           poi_lat = a.poi.location.lat,
                           poi_lon = a.poi.location.lon,
                           poi_id = a.poi.id,
                           places_reference = a.poi.google_places_reference,
                           modified = int(mktime(a.modified.utctimetuple())),
                           created = int(mktime(a.created.utctimetuple())),
                           username = a.username,
                           lists = [List(id=l['id'], name=l['name']) for l in lists if s.id in l['keys']],
                           id = a.id,
                         )
            response.append(t)
        return Suggestions(query_id='', suggestions=response)
    
    
    @remote.method(GetSuggestionRequest, Suggestion)
    def get_suggestion(self, request):
        user = User.objects.get_by_id(int(environ['user']))
        from geovote.api import get_comments
        suggestion = SuggestionModel.objects.get_by_id_querier(request.id, querier=user)
        lists = ListSuggestion.objects.get_by_user(user=user, querier=user, all=True)
        query_id, comments_async = get_comments(user, suggestion.id, 'Event', async=True)
        suggestion = single_prefetch_refprops(suggestion, SuggestionModel.user, SuggestionModel.poi)
        has_voted = Vote.objects.user_has_voted(user, suggestion.key())
        vote_counter = Vote.objects.get_vote_counter(suggestion.key())
        user_follower = suggestion.has_follower(user)
        top_comments = Comment.objects.get_top_voted(suggestion, user)
        in_lists = ListSuggestion.objects.get_by_suggestion(suggestion, user)
        # construir un diccionario con todas las keys resueltas y usuarios
        in_lists = [l.to_dict(resolve=False) for l in in_lists]
        # listas del usuario
#        lists = [l for l in lists if not suggestion.key() in l.keys]
#        lists = prefetch_refprops(lists, ListSuggestion.user)
#        lists = [l.to_dict(resolve=False) for l in lists]
        comments = Comment.objects.load_comments_from_async(query_id, comments_async, user)
        return Suggestion(id = suggestion.id,
                          name=suggestion.name,
                          description=suggestion.description,
                          poi_lat=suggestion.poi.location.lat,
                          poi_lon=suggestion.poi.location.lon,
                          poi_id=suggestion.poi.id,
                          places_reference = suggestion.poi.google_places_reference,
                          modified = int(mktime(suggestion.modified.utctimetuple())),
                          created = int(mktime(suggestion.created.utctimetuple())),
                          username = suggestion.username,
                          lists = [List(id=l['id'], name=l['name']) for l in in_lists],
                          comments = [Comment(id=c['id']) for c in comments],
                          has_voted=has_voted,
                          lists=lists,
                          vote_counter= vote_counter,
                          user_follower= user_follower,
                          top_comments= top_comments,
                         )
#    @remote.method(GetSyncSuggestion, Suggestions)
#    def sync_suggestions(self, request):
#        if len(request.suggestions) > 20:
#            from protorpc.remote import ApplicationError
#            raise ApplicationError("Too many suggestions")
#        from os import environ
#        user= environ['user']
#        from datetime import datetime
#        from time import mktime
#        if request.last_sync is None:
#            request.last_sync = int(mktime(user.created.utctimetuple()))
#        from geoalert.models import Suggestion as SuggestionModel
#        from geoalert.models_poi import Place as PlaceModel
#        from google.appengine.ext import db
#        clients_ids = []
#        suggestions_to_save = []
#        for a in request.suggestions:
#            id = a.get('id', None)
#            if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
#                old = SuggestionModel.objects.get_by_id_user(id, request.user)
#                if not old:  # no existe en la BD, fue borrada.
#                    continue
#            poi = PlaceModel.get_or_insert(location = a.poi_id,
#                                      google_places_reference=a.places_reference,
#                                      user = request.user)
#            s = SuggestionModel.update_or_insert(
#                         id = id,
#                         name = a.get('name', u''),
#                         description = a.get('description', u''),
#                         user = user,
#                         poi = poi,
#                         commit = False
#                         )
#            suggestions_to_save.append(s) # juntamos para hacer un solo put
#            clients_ids.append(a.client_id) # la alerta no estaba sincronizada
#        db.put(suggestions_to_save)
#        suggestions = SuggestionModel.objects.get_by_last_sync(user,
#                                                     datetime.fromtimestamp(request.last_sync)
#                                                     )
#        response = [Suggestion(
#                           name = a.name,
#                           description = a.description,
#                           poi_lat = a.poi.location.lat,
#                           poi_lon = a.poi.location.lon,
#                           poi_id = a.poi.id,
#                           places_reference = a.poi.google_places_reference,
#                           modified = int(mktime(a.modified.utctimetuple())),
#                           created = int(mktime(a.created.utctimetuple())),
#                           id = a.id,
#                         ) for a in suggestions]
#        for a, b in zip(response, clients_ids):
#            if b is not None:
#                response.client_id = b
#        return Suggestions(suggestions=response)