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
    
    
class GetSuggestionsNearestRequest(messages.Message):
    lat = messages.IntegerField(1)
    lon = messages.IntegerField(2)
    radius = messages.IntegerField(3, default=5000)
    

class GetSuggestionRequest(messages.Message):
    id = messages.IntegerField(1, required=True)
    
class GetSuggestionsNearestRequest(messages.Message):
    lat = messages.IntegerField(1)
    lon = messages.IntegerField(2)
    radius = messages.IntegerField(3, default=5000)
    

class SuggestionService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSuggestionsRequest, Suggestions)
    def get_suggestions(self, request):
        """
            Obtiene la mochila del usuario con la sesion iniciada
           
               Recibe: :class:`GetSuggestionsRequest
               Devuelve: :class:`Suggestions`
        """
        user = User.objects.get_by_id(int(environ['user']))
        lists_following = ListSuggestion.objects.get_list_user_following(user, async=True)
        lists = ListSuggestion.objects.get_by_user(user=user, querier=user, all=True)
        from geoalert.api import get_suggestions_dict
        suggestions = get_suggestions_dict(request.user)
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
                           google_places_reference = a.poi.google_places_reference,
                           modified = int(mktime(a.modified.utctimetuple())),
                           created = int(mktime(a.created.utctimetuple())),
                           username = a.user.username,
                           lists = [List(id=l['id'], name=l['name']) for l in lists if a.id in l['keys']],
                           id = a.id,
                         )
            response.append(t)
        return Suggestions(query_id='', suggestions=response)
    
    
    @remote.method(GetSuggestionRequest, Suggestion)
    def get_suggestion(self, request):
        """
            Devuelve la informacion sobre una sugerencia
           
               Recibe: :class:`GetSuggestionRequest
               Devuelve: :class:`Suggestion`
        """
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
        comments = Comment.objects.load_comments_from_async(query_id, comments_async, user)[1]
        return Suggestion(id = suggestion.id,
                          name=suggestion.name,
                          description=suggestion.description,
                          poi_lat=suggestion.poi.location.lat,
                          poi_lon=suggestion.poi.location.lon,
                          poi_id=suggestion.poi.id,
                          google_places_reference = suggestion.poi.google_places_reference,
                          modified = int(mktime(suggestion.modified.utctimetuple())),
                          created = int(mktime(suggestion.created.utctimetuple())),
                          username = suggestion.user.username,
                          lists = [List(id=l['id'], name=l['name']) for l in in_lists],
                          comments = [Comment(id=c['id']) for c in comments],
                         )
        
    @remote.method(GetSuggestionsNearestRequest, Suggestions)
    def get_nearest(self, request):
        user = User.objects.get_by_id(int(environ['user']))
        suggestions = SuggestionModel.objects.get_nearest(db.GeoPt(request.lat, request.lon),
                                                          radius=request.radius,
                                                          querier=user
                                                          )
        response = []
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
        response.append(t)
        return Suggestions(query_id='', suggestions=response)
