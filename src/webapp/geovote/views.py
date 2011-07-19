# coding=utf-8

from models import *
from geouser.decorators import login_required
from geoalert.models import Suggestion
from geolist.models import *

#===============================================================================
# COMENTARIOS
#===============================================================================
@login_required
def do_comment_event(request, instance_id, msg):
    """
    Realiza un comentario a una sugerencia
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param msg: mensaje del comentario
        :type msg: :class:`string`
    """
    user = request.session['user']
    event = Event.objects.get_by_id_user(id=instance_id, user=user)
    if event is None:
        return None
    comment = Comment.do_comment(user=user, instance=event, msg=msg)
    
    return comment


@login_required
def do_comment_list(request, instance_id, msg):
    """
    Realiza un comentario a una lista
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param msg: mensaje del comentario
        :type msg: :class:`string`
    """
    user = request.session['user']
    list = List.objects.get_by_id_user(id=instance_id, user=user)
    if list is None:
        return None
    comment = Comment.do_comment(user=user, instance=list, msg=msg)

    return comment


def get_comments_event(request, instance_id, query_id=None, page=1):
    """
    Obtiene los comentarios de cualquier evento visible
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
        :param query_id: identificador de la busqueda paginada
        :type query_id: :class:`long`
        :param page: pagina a buscar
        :type page: :class:`integer`
    """
    user = request.session.get('user', None)
    if user is not None:
        event = Event.objects.get_by_id_user(instance_id, user)
    else:
        event = Event.objects.get_by_id(instance_id)
    if event is None:
        return None
    
    return _get_comments(event, query_id=query_id, page=page)


def get_comments_list(request, instance_id, query_id=None, page=1):
    """
    Obtiene los comentarios de cualquier lista visible
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
        :param query_id: identificador de la busqueda paginada
        :type query_id: :class:`long`
        :param page: pagina a buscar
        :type page: :class:`integer`
    """
    user = request.session.get('user', None)
    if user is not None:
        list = List.objects.get_by_id_user(instance_id, user)
    else:
        list = List.objects.get_by_id(instance_id)
    if list is None:
        return None
    
    return _get_comments(list, query_id=query_id, page=page)        


def _get_comments(instance, query_id=None, page=1):
    """
    Obtiene los comentarios de cualquier objeto
    
        :param instance_key: Clave del objeto
        :type instance_key: :class:`db.Key`
        :param query_id: identificador de la busqueda paginada
        :type query_id: :class:`long`
        :param page: pagina a buscar
        :type page: :class:`integer`
        
    """
    comments = Comment.objects.get_by_instance(instance, query_id=query_id, page=page)
    
    return comments
    
#===========================================================================
# VOTACIONES
#===========================================================================
@login_required
def do_vote_suggestion(request, instance_id, vote):
    """
    Realiza un voto a una sugerencia
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param vote: valoracion del voto (siempre positivo)
        :type vote: :class:`integer`
    """
    user = request.session['user']
    event = Suggestion.objects.get_by_id_user(id=instance_id, user=user, querier=request.user)
    if event is None:
        return None
    vote = Vote.do_vote(user=user, instance=event, count=vote)
    
    return vote


@login_required
def do_vote_list(request, instance_id, vote):
    """
    Realiza un voto a una lista
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param vote: valoracion del voto (siempre positivo)
        :type vote: :class:`integer`
    """
    user = request.session['user']
    list = List.objects.get_by_id_user(id=instance_id, user=user)
    if list is None:
        return None
    vote = Vote.do_vote(user=user, instance=list, count=vote)
    
    return vote


@login_required
def do_vote_comment(request, instance_id, vote):
    """
    Realiza un voto a una lista
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param vote: valoracion del voto (siempre positivo)
        :type vote: :class:`integer`
    """
    user = request.session['user']
    comment = Comment.objects.get_by_id_user(id=instance_id, user=user)
    if comment is None:
        return None
    vote = Vote.do_vote(user=user, instance=comment, count=vote)
    
    return vote


def get_vote_suggestion(request, instance_id):
    """
    Obtiene el contador de votos de una sugerencia
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
    """
    user = request.session['user']
    if user is not None:
        suggestion = Suggestion.objects.get_by_id_user(instance_id, user)
    else:
        suggestion = Suggestion.objects.get_by_id(instance_id)
    if suggestion is None:
        return None
    return _get_vote(suggestion.key())

    
def get_vote_list(request, instance_id):
    """
    Obtiene el contador de votos de una lista
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
    """
    user = request.session['user']
    if user is not None:
        list = List.objects.get_by_id_user(instance_id, user)
    else:
        list = List.objects.get_by_id(instance_id)
    if list is None:
        return None
    return _get_vote(list.key())


def get_vote_comment(request, instance_id):
    """
    Obtiene el contador de votos de un comentario
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
    """
    user = request.session['user']
    if user is not None:
        comment = Comment.objects.get_by_id_user(instance_id, user)
    else:
        comment = Comment.objects.get_by_id(instance_id)
    if suggestion is None:
        return None
    return _get_vote(comment.key())

    
def _get_vote(instance_key):
    Vote.objects.get_vote_counter(instance_key)
    
    return counter
    
