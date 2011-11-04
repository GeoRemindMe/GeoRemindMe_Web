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
.. module:: api/messages
    :platform: google-appengine (GAE)
    :synopsis: Mensajes de respuesta que envia la API
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""


from protorpc import messages

    
class LoginResponse(messages.Message):
    """
    Respuesta correcta a una peticion de login,
        se iniciara una sesion nueva.
        
        :param session: Identificador de la sesion
        :type session: :class:`String`
        :param expires: Tiempo (en segundos) que dura la sesion
        :type expires: :class:`Integer`
    """
    session = messages.StringField(1)
    expires = messages.IntegerField(2)


class Timeline(messages.Message):
    """
    Estructura que contiene la informacion devuelta
        de un solo timeline
        
            :param msg: mensaje del timeline (OPCIONAL)
            :type msg: :class:`string`
            :param msg_id: identificador del tipo de mensaje
            :type msg_id: :class:Ìnteger`
            :param instance_id: identificador del objeto al que
                se refiere el timeline (OPCIONAL)
            :type instance_id: :class:`Integer`
            :param instance_name: nombre del objeto al que se 
                refiere el timeline (OPCIONAL)
            :type instance_name: :class:`String`
            :param url: url del objeto (OPCIONAL)
            :type url: :class:`String`
            :param user: nombre del usuario dueño del timeline
            :type user: :class:`string`
            :param created: tiempo en segundos en el que se creo 
                el timeline
            :type created: :class:`Integer`
    """
    msg = messages.StringField(1)
    msg_id = messages.IntegerField(2)
    instance_id = messages.IntegerField(3)
    instance_name = messages.StringField(4)
    url = messages.StringField(5)
    user = messages.StringField(6)
    created = messages.IntegerField(7)
    

class Timelines(messages.Message):
    """
    Contendra todos los timelines que se esten devolviendo en la consulta
        
        :param timelines: lista con todos los timelines devueltos
        :type timelines: :class:`messages.Timeline`
        :param query_id: Identificador para continuar con la consulta
        :type query_id: :class:`String`
    """
    timelines = messages.MessageField(Timeline, 1, repeated=True)
    query_id = messages.StringField(2)
    

class List(messages.Message):
    """
    Informacion sobre una lista
        
        :param id: Identificador de la lista
        :type id: :class:`Integer`
        :param name: Nombre de la lista
        :type name: :class:`String`
    """
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    

class Comment(messages.Message):
    """
    Contiene un comentario
        
        :param id: Identificador del comentario
        :type id: :class:`Integer` identificador del comentario
        :param username: nombre del usuario que escribio el comentario
        :type username: :class:`String`
        :param message: mensaje escrito
        :type message: :class:`String`
        :param created: tiempo en segundos desde que se creo el comentario
        :type created: :class:`Integer`
    """
    id = messages.IntegerField(1)
    username = messages.StringField(2)
    msg = messages.StringField(3)
    created = messages.IntegerField(4)
    
    
class Suggestion(messages.Message):
    """
        Contiene una sugerencia
        
            :param name:  nombre de la sugerencia
            :type name: :class:`String`
            :param description: descripcion de la sugerencia 
            :type description: :class:`String`
            :param poi_lat: latitud del punto donde esta la sugerencia
            :type poi_lat: :class:`Float`
            :param poi_lon: longitud del punto donde esta la sugerencia
            :type poi_lon: :class:`Float`
            :param poi_id: identificador del punto donde esta la sugerencia
            :type poi_id: :class:`Integer`
            :param google_places_reference: identificador del lugar en google places
            :type google_places_reference: :class:`String`
            :param created: tiempo en segundos desde que se creo la sugerencia
            :type created: :class:`Integer`
            :param modified: tiempo en segundos desde que se modifico por ultima
                vez la sugerencia
            :type modified: :class:`Integer`
            :param username: nombre del usuario que creo la sugerencia
            :type username: :class:`String`
            :param id: identificador unico de la sugerencia
            :type id: :class:`Integer`
            :param lists: contiene las listas a las que pertenece la sugerencia
            :type lists: :class:`messages.List`
            :param comments: contiene todos los comentarios de la sugerencia
            :type comments: :class:`messages.Comment`
            :param has_voted: True si el usuario ha votado
            :type has_voted: :class:`Boolean`
            :param vote_counter: contador de votos recibidos por la sugerencia
            :type vote_counter: :class:`Integer`
            :param user_follower: True si el usuario ya sigue la sugerencia
            :type user_follower: :class:`Boolean`
            :param top_comments: Commentarios mas votados
            :type top_comments: :class:`messages.Comment` 
    """
    name = messages.StringField(1, required=True)
    description = messages.StringField(2)
    poi_lat = messages.FloatField(3)
    poi_lon = messages.FloatField(4)
    poi_id = messages.IntegerField(5)
    google_places_reference = messages.StringField(6)
    created = messages.IntegerField(7)
    modified = messages.IntegerField(8)
    username = messages.StringField(9)
    id = messages.IntegerField(10)
    lists = messages.MessageField(List, 11, repeated=True)
    comments = messages.MessageField(Comment, 13, repeated=True)
    has_voted = messages.BooleanField(14)
    vote_counter = messages.IntegerField(15)
    user_follower = messages.BooleanField(16)
    top_comments = messages.MessageField(Comment, 17, repeated=True)
    

class Suggestions(messages.Message):
    """
        Contendra una lista de sugerencias que se esten devolviendo en la consulta
        
            :param suggestions: Lista de sugerencias
            :type suggestions: :class:`messages.Suggestions`
            :param query_id: Identificador para continuar con la consulta
            :type query_id: :class:`String`
    """
    query_id = messages.StringField(1)
    suggestions = messages.MessageField(Suggestion, 2, repeated=True)
    

class Site(messages.Message):
    """
        Informacion de un sitio a devolver con el autocompletado
        
            name: :class:`string` nombre devuelto por Places
            address: :class:`string` direccion devuelta por Places
            lat: :class:`float`
            lon: :class:`float`
    """
    name = messages.StringField(1, required=True)
    address = messages.StringField(2)
    lat = messages.FloatField(3)
    lon = messages.FloatField(4)
    
    
class Sites(messages.Message):
    """
        Coleccion de sitios devueltos por Places
    """
    sites = messages.MessageField(Site, 1, repeated=True)


class Place(messages.Message):
    """
        Informacion de un sitio:
        
            name: :class:`string` nombre de la sugerencia
            address: :class:`string`
            city: :class:`string`
            poi_lat: :class:`float`
            poi_lon: :class:`float`
            google_places_reference: :class:`string`
            id: :class:`integer`
            vote_counter: :class:`integer`
            suggestions: :class:`Suggestions` lista con los suggerencias
    """ 
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    address = messages.StringField(3)
    city = messages.StringField(4)
    suggestions = messages.MessageField(Suggestions, 5)
    poi_lat = messages.FloatField(6)
    poi_lon = messages.FloatField(7)
    vote_counter = messages.IntegerField(8)
    google_places_reference = messages.StringField(9)
    