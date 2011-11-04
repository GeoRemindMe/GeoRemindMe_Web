# coding:utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the Affero General Public License (AGPL) as published 
by Affero, as published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

You should have received a copy of the GNU Affero General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""

"""
.. module:: api/suggestionservice
    :platform: google-appengine (GAE)
    :synopsis: Funciones para obtener sugerencias del usuario (mochila, sugerencia, etc.)
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Suggestion, Suggestions, List

from time import mktime
from os import environ

from mainservice import MainService
from geoalert.api import get_suggestions_dict
from geoalert.models import Suggestion as SuggestionModel
from geouser.models import User
from geolist.models import ListSuggestion
from geovote.models import Vote, Comment
from google.appengine.ext import db
from georemindme.funcs import prefetch_refprops, prefetch_refList, single_prefetch_refprops


class GetSuggestionsRequest(messages.Message):
    """
    Obtiene la mochila completa del usuario.
            
        :param query_id: (NO USABLE) identificador para continuar una peticion anterior, 
            si no existe, se devuelve la mochila con las sugerencias mas nuevas
        :type query_id: :class`String`
        :param page: (NO USABLE) pagina a obtener de la mochila 
        :type limit: :class:`Integer`
    """
    query_id = messages.StringField(1)
    page = messages.IntegerField(2, default=1)
    
    
class GetSuggestionsNearestRequest(messages.Message):
    """
    Obtiene las sugerencias mas cercanas al usuario
    
        :param lat: latitud en la que se encuentra el usuario
        :type lat: :class:`Float`
        :param lon: longitud en la que se encuentra el usuario
        :type lon: :class:`Float`
        :param radius: radio de distancia maxima en la que buscar
            (en metros, 5000 por defecto, opcional)
        :type radius: :class:`Integer`
    """
    lat = messages.FloatField(1, required=True)
    lon = messages.FloatField(2, required=True)
    radius = messages.IntegerField(3, default=5000)
    

class GetSuggestionRequest(messages.Message):
    """
    Obtiene la sugerencia especificada por el ID
    
        :param id: Identificador de la sugerencia
        :type id: :class:`Integer`
    """
    id = messages.IntegerField(1, required=True)
    

class SuggestionService(MainService):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetSuggestionsRequest, Suggestions)
    def get_suggestions(self, request):
        """
        Obtiene la mochila del usuario con la sesion iniciada
           
            :param request: Parametros pasados a la peticion
            :type request: :class:`GetSuggestionsRequest`
            :returns: :class:`Suggestions`
        """
        self._login_required()
        
        lists_following = ListSuggestion.objects.get_list_user_following(self.user, async=True)
        from geoalert.api import get_suggestions_dict
        suggestions = get_suggestions_dict(self.user)
        lists = ListSuggestion.objects.load_list_user_following_by_async(lists_following, to_dict=False, resolve=False)
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
                           lists = [List(id=l.id, name=l.name) for l in lists if a.key() in l.keys],
                           id = a.id,
                         )
            response.append(t)
        return Suggestions(query_id='', suggestions=response)
    
    
    @remote.method(GetSuggestionRequest, Suggestion)
    def get_suggestion(self, request):
        """
        Obtiene la informacion de la sugerencia solicitada
           
            :param request: Parametros pasados a la peticion
            :type request: :class:`GetSuggestionRequest`
            :returns: :class:`Suggestion`
            :raises: :class:`ApplicationError`
        """
        self._login_required()
        
        from geovote.api import get_comments
        suggestion = SuggestionModel.objects.get_by_id_querier(request.id, querier=self.user)
        query_id, comments_async = get_comments(self.user, suggestion.id, 'Event', async=True)
        suggestion = single_prefetch_refprops(suggestion, SuggestionModel.user, SuggestionModel.poi)
        has_voted = Vote.objects.user_has_voted(self.user, suggestion.key())
        vote_counter = Vote.objects.get_vote_counter(suggestion.key())
        user_follower = suggestion.has_follower(self.user)
        top_comments = Comment.objects.get_top_voted(suggestion, self.user)
        in_lists = ListSuggestion.objects.get_by_suggestion(suggestion, self.user)
        in_lists = [l.to_dict(resolve=False) for l in in_lists]
        comments = Comment.objects.load_comments_from_async(query_id, comments_async, self.user)[1]
        # TODO: ENVIAR LOS COMENTARIOS AL MOVIL
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
                          comments = [Comment(id=c['id'],
                                              username=c['username'],
                                              message=c['msg'],
                                              created=c['created']) for c in comments],
                          has_voted=has_voted,
                          vote_counter=vote_counter,
                          user_follower=user_follower,
                         )
        
    @remote.method(GetSuggestionsNearestRequest, Suggestions)
    def get_nearest(self, request):
        """
        Obtiene una lista con sugerencias cercanas
           
            :param request: Parametros pasados a la peticion
            :type request: :class:`GetSuggestionsNearestRequest`
            :returns: :class:`Suggestions`
            :raises: :class:`ApplicationError`
        """
        self._login_required()
        
        suggestions = SuggestionModel.objects.get_nearest(db.GeoPt(request.lat, request.lon),
                                                          radius=request.radius,
                                                          querier=self.user
                                                          )
        response = []
        for a in suggestions:
            t = Suggestion(
                           name = a['name'],
                           description = a['description'],
                           poi_lat = a['poi']['lat'],
                           poi_lon = a['poi']['lon'],
                           poi_id = a['poi']['id'],
                           modified = int(mktime(a['modified'].utctimetuple())),
                           created = int(mktime(a['created'].utctimetuple())),
                           username = a['username'],
                           id = a['id'],
                         )
        response.append(t)
        return Suggestions(query_id='', suggestions=response)
