# coding=utf-8

from geouser.decorators import login_required
from models import *

#===============================================================================
# CREACION DE LISTAS
#===============================================================================
@login_required
def new_list_user(request, name, description = None, instances = []):
    '''
    Crea una nueva lista de usuarios
        
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de usuarios iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    '''
    list = ListUser.insert_list(user=request.session['user'], name=name, description=description, instances=instances)
    return list.id

@login_required
def new_list_alert(request, name=None, description=None, instances=None):
    '''
    Crea una nueva lista de alertas
        
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de alertas iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    '''
    list = ListAlert.insert_list(user=request.session['user'], name=name, description=description, instances=instances)
    return list.id

#===============================================================================
# Modificacion de listas
#===============================================================================
@login_required
def mod_list_user(request, id, name=None, description=None, instances_add=[], instances_del=[]):
    '''
    Modifica una lista de usuarios
        
        :param id: identificador de la lista
        :type id: :class:`integer`
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de alertas iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista modificada
    '''
    list = ListUser.objects.get_by_id_user(id, user)
    if list is not None:
        list.update(name=name, description=description, instances_add=instances_add, instances_del=instances_del)
        return True
    return False

@login_required
def mod_list_alert(request, id, name=None, description=None, instances_add=[], instances_del=[]):
    '''
    Modifica una lista de alertas
        
        :param id: identificador de la lista
        :type id: :class:`integer`
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de alertas iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista modificada
    '''
    list = ListAlert.objects.get_by_id_user(id, user)
    if list is not None:
        list.update(name=name, description=description, instances_add=instances_add, instances_del=instances_del)
        return True
    return False

#===============================================================================
# Obtiene listas
#===============================================================================
def get_list(request, id = None, user = None):
    '''
    Obtiene una lista por el identificador
        
        :param id: identificador de la lista
        :type id: :class:`integer`
        :returns: id de la lista modificada
    '''
    
    user = request.session.get('user', None)
    list = List.objects.get_by_id_user(id = id, user = user)
    return list

@login_required
def get_list_user(request, id = None, name = None):
    '''
    Obtiene una lista de usuarios
        
        :param id: identificador de la lista
        :type id: :class:`integer`
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :returns: id de la lista modificada
    '''
    user = request.session['user']
    if id is not None:
        list = ListUser.objects.get_by_id_user(id, user)
    elif name is not None:
        list = ListUser.objects.get_by_name_user(name, user)
    else:
        raise TypeError()
    
    return list


@login_required
def get_list_alert(request, id = None, name = None):
    '''
    Obtiene una lista de alertas
        
        :param id: identificador de la lista
        :type id: :class:`integer`
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :returns: id de la lista modificada
    '''
    user = request.session['user']
    if id is not None:
        list = ListAlert.objects.get_by_id_user(id, user)
    elif name is not None:
        list = ListAlert.objects.get_by_name_user(name, user)
    else:
        raise TypeError()
    
    return list

@login_required
def del_list(request, id):
    '''
    Borra una lista
    Parametros POST
        :param id: identificador de la lista
        :type id: :class:`integer`
        
        :returns: True si se borro la lista
    '''
    user = request.session['user']
    list = List.objects.get_by_id_user(id, user = user)
    if list.user == user:
        list.active = False
        list.put()
        return True
    return False