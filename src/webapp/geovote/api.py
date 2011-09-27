# coding=utf-8

"""
.. module:: views
    :platform: appengine
    :synopsis: Vistas para obtener comentarios y votos
"""


from models import Comment, Vote
from geouser.decorators import login_forced


#===============================================================================
# COMENTARIOS
#===============================================================================
@login_forced
def do_comment(querier, instance_id, kind, msg):
    """
    Realiza un comentario a una sugerencia
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param msg: mensaje del comentario
        :type msg: :class:`string`
    """
    if not kind in ['Event', 'List']:
        return None
    try:
        instance_id = int(instance_id)
    except:
        return None
    from geoalert.models import Event
    from geolist.models import List
    from geovote.models import Comment
    obj = eval(kind).get_by_id(instance_id)
    if obj is None:
        return None
    if obj.__class__.user.get_value_for_datastore(obj) != querier.key():
        if hasattr(obj, '_vis'):
            if obj._is_private():
                return None
            elif obj._is_shared() and not obj.user_invited(querier):
                return None
        else:
            return None
    comment = Comment.do_comment(user=querier, instance=obj, msg=msg)
    return comment


def get_comments(querier, instance_id, kind, query_id=None, page=1, async=False):
    """
    Obtiene los comentarios de cualquier evento visible
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
        :param query_id: identificador de la busqueda paginada
        :type query_id: :class:`long`
        :param page: pagina a buscar
        :type page: :class:`integer`
    """
    if not kind in ['Event', 'List']:
        return None
    try:
        instance_id = int(instance_id)
    except:
        return None
    from geoalert.models import Event
    from geolist.models import List
    from geovote.models import Comment
    obj = eval(kind).get_by_id(instance_id)
    if obj is None:
        return None
    if obj.__class__.user.get_value_for_datastore(obj) != querier.key():
        if hasattr(obj, '_vis'):
            if obj._is_private():
                return None
            elif obj._is_shared() and not obj.user_invited(querier):
                return None
        else:
            return None
    return _get_comments(obj, query_id=query_id, page=page, querier=querier, async=async)


def _get_comments(instance, query_id=None, page=1, querier=None, async=False):
    """
    Obtiene los comentarios de cualquier objeto
    
        :param instance_key: Clave del objeto
        :type instance_key: :class:`db.Key`
        :param query_id: identificador de la busqueda paginada
        :type query_id: :class:`long`
        :param page: pagina a buscar
        :type page: :class:`integer`
        
    """
    if querier.is_authenticated():
        return Comment.objects.get_by_instance(instance, query_id=query_id, page=page, querier=querier, async=async)
    else:
        return Comment.objects.get_by_instance(instance, query_id=query_id, page=page, async=async)


#===========================================================================
# VOTACIONES
#===========================================================================

@login_forced
def do_vote(querier, kind, instance_id, vote=1):
    """
    Realiza un voto a un comentarion
    
        :param instance_id: ID del objeto a comentar
        :type instance_id: :class:`long`
        :param vote: valoracion del voto
        :type vote: :class:`integer`
    """
    if not kind in ['Event', 'List', 'Comment']:
        return None
    vote = int(vote)
    if vote > 1 or vote < -1:
        return False
    from geoalert.models import Event
    from geolist.models import List
    from geovote.models import Comment
    try:
        obj = eval(kind).objects.get_by_id(instance_id)
    except:
        return None
    if obj is None:
        return None
    if obj.__class__.user.get_value_for_datastore(obj) != querier.key():
        if hasattr(obj, '_vis'):
            if obj._is_private():
                return None
            elif obj._is_shared() and not obj.user_invited(querier):
                return None
        else:
            return None
    else: # no se puede votar lo de uno mismo
        return None
    vote = Vote.do_vote(user=querier, instance=obj, count=vote)
    return {'vote': vote, 'votes': _get_vote(obj.key())}


def get_votes(querier, kind, instance_id):
    """
    Obtiene el contador de votos de un comentario
    
        :param instance_id: ID del evento
        :type instance_key: :class:`long`
    """
    if not kind in ['Event', 'List', 'Comment']:
        return None
    try:
        instance_id = int(instance_id)
    except:
        return None
    from geoalert.models import Suggestion
    from geolist.models import List
    from geovote.models import Comment
    obj = eval(kind).get_by_id(instance_id)
    if obj is None:
        return None
    if obj.__class__.user.get_value_for_datastore(obj) != querier.key():
        if hasattr(obj, '_vis'):
            if obj._is_private():
                return None
            elif obj._is_shared() and not obj.user_invited(querier):
                return None
        else:
            return None
    return _get_vote(obj.key())

    
def _get_vote(instance_key):
    counter = Vote.objects.get_vote_counter(instance_key)
    return counter
    

@login_forced    
def delete_comment(querier, comment_id):
    """
    Borra un comentario, realizado por el usuario
    
        :param comment_id: ID del evento
        :type comment_id: :class:`long`
    """
    comment = Comment.objects.get_by_id_user(comment_id, querier)
    if comment is not None:
        comment.delete()
        return True
    return False
