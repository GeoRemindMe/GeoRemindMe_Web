# coding=utf-8

from geouser.decorators import login_forced

#===============================================================================
# FUNCIONES DE FOLLOWERS Y FOLLOWINGS
#===============================================================================
def get_followers(querier, userid=None, username=None, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de followers de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado.
        
        :param userid: id del usuario (user.id)
        :type userid: string
        :param username: nombre del usuario (user.username)
        :type username: string
        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    if userid is None and username is None:
        if querier.is_authenticated():
            return querier.get_followers(page=page, query_id=query_id)
        return None
    else:
        from models import User
        from models_acc import UserSettings
        if userid:
            profile_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            profile_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(profile_key.name())
        if settings.show_followers:
            return User.objects.get_followers(userid=userid, username=username, page=page, query_id=query_id)
    return None


def get_followings(querier, userid=None, username=None, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de followings de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado
        
        :param userid: id del usuario (user.id)
        :type userid: string
        :param username: nombre del usuario (user.username)
        :type username: string
        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    if userid is None and username is None:
        if querier.is_authenticated():
            return querier.get_followings(page=page, query_id=query_id)
        return None
    else:
        from models import User
        from models_acc import UserSettings
        if userid:
            user_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            user_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(user_key.name())
        if settings.show_followings:
            return User.objects.get_followings(userid=userid, username=username, page=page, query_id=query_id)
    return None


@login_forced
def add_following(querier, userid=None, username=None):
    """**Descripción**:    Añade un  nuevo usuario a la lista de following del usuario logeado
    
        :param userid: id del usuario (user.id)
        :type userid: string
        :param username: nombre del usuario (user.username)
        :type username: string
        :return: booleano con el resultado de la operación
    """
    return querier.add_following(followid=userid, followname=username)


@login_forced
def del_following(querier, userid=None, username=None):
    """**Descripción**: Borra un usuario de la lista de following del usuario logeado
        
        :param userid: id del usuario (user.id)
        :type userid: string
        :param username: nombre del usuario (user.username)
        :type username: string
        :return: boolean con el resultado de la operacion
    """
    return querier.del_following(followid=userid, followname=username)


#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
def get_profile_timeline(querier, userid = None, username = None, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado
        
        :param userid: id del usuario (user.id)
        :type userid: string
        :param username: nombre del usuario (user.username)
        :type username: string
        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad            
    """
    if userid is None and username is None:
        if querier.is_authenticated():
            return querier.get_profile_timeline(query_id=query_id)
        return None
    else:
        from models import User
        if userid:
            user_profile = User.objects.get_by_id(userid)
        elif username:
            user_profile = User.objects.get_by_username(username)
        if user_profile.settings.show_timeline:
            return user_profile.get_profile_timeline(query_id=query_id, querier=querier)
    return None


@login_forced
def get_activity_timeline(querier, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de actividad del usuario logueado

        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    return querier.get_activity_timeline(query_id=query_id)


@login_forced
def get_notifications_timeline(querier, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de actividad del usuario logueado

        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    querier.counters.set_notifications(-10)
    return querier.get_notifications_timeline(query_id=query_id)
