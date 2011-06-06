# coding=utf-8

from datetime import timedelta, datetime
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from google.appengine.api import users

from funcs import getAlertsJSON, getListsJSON
from decorators import ajax_request
from geouser.models import User
import geouser.views as geouser
from geouser.funcs import init_user_session, login_func
from geoalert.forms import *
from geoalert.models import *
import geoalert.views as geoalert
import geolist.views as geolist


@ajax_request
def exists(request):
    
    if not request.POST.get('email'):
        return HttpResponseBadRequest()
    user = User.objects.get_by_email( request.POST.get('email') )
    if user:
        return HttpResponse('{"result":"exists"}',mimetype="application/json")
    else:
        return HttpResponse('{"result":""}',mimetype="application/json")


@ajax_request
def register(request):
    from geouser.views import register
    user, f = register(request)
    data = {}
    if user:  # user registrado, iniciamos sesion
        data['error'], data['_redirect'] = login_func(request, user = user)
        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    data['errors'] = f.errors
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


@ajax_request
def contact(request):
    from georemindme.geomail import send_contact_email
    send_contact_email(request.POST.get('userEmail',''),request.POST.get('msg',''))
    
    return HttpResponse()


@ajax_request
def keepuptodate(request):
    
    from georemindme.geomail import send_keepuptodate
    
    data = ''
    for k in request.POST.keys():
        if k.endswith("version"):
            data+=(k+"<br/>")

    send_keepuptodate(request.POST.get('user-email',''),data)
    
    return HttpResponse()


@ajax_request
@never_cache
def login(request):
    from geouser.views import login
    data = {}
    data['error'], data['_redirect'] = login(request)
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


#===============================================================================
# FUNCIONES AJAX PARA OBTENER, MODIFICAR, BORRAR ALERTAS
#===============================================================================
@ajax_request
def add_reminder(request):
    form = RemindForm(request.POST)
    if form.is_valid():
        id = request.POST.get('id', None)
        if id:
            alert = geoalert.edit_alert(request, request.POST.get('id'), form, request.POST['address'])
        else: 
            alert = geoalert.add_alert(request, form, address=request.POST['address'])
        return HttpResponse(simplejson.dumps(dict(id=alert.id)), mimetype="application/json")
    else:
        return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")

@ajax_request
def get_reminder(request):
    id = request.POST.get('id', None)
    done = request.POST.get('done', None)
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    alerts = geoalert.get_alert(request, id, done, page, query_id)
    return HttpResponse(getAlertsJSON(alerts), mimetype="application/json")

@ajax_request
def delete_reminder(request):
    id = request.POST.get('id', None)
    geoalert.del_alert(request, id)    
    return HttpResponse()


#===============================================================================
# FUNCIONES AJAX PARA OBTENER FOLLOWERS Y FOLLOWINGS
#===============================================================================
@ajax_request
def get_followers(request):
    '''
        Devuelve la lista de followers de un usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma (id, username)
    ''' 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    userid = request.POST.get('id', None)
    username = request.POST.get('username', None)
    followers = geouser.get_followers(request, userid, username, page, query_id)
    return HttpResponse(simplejson.dumps(followers), mimetype="application/json")  # los None se parsean como null

@ajax_request
def get_followings(request):
    '''
        Devuelve la lista de followings de un usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma (id, username)
    ''' 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    userid = request.POST.get('id', None)
    username = request.POST.get('username', None)
    followings = geouser.get_followings(request, userid, username, page, query_id)
    return HttpResponse(simplejson.dumps(followings), mimetype="application/json")

@ajax_request
def add_following(request):
    '''
        Añade a la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
       
            :returns: boolean
    ''' 
    userid = request.POST.get('id', None)
    username = request.POST.get('username', None)
    added = geouser.add_following(request, userid=userid, username=username)
    return HttpResponse(simplejson.dumps(added), mimetype="application/json")
    
@ajax_request
def del_following(request):
    '''
        Borra de la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a borrar
            username : el username del usuario a borrar
       
            :returns: boolean
    '''
    userid = request.POST.get('id', None)
    username = request.POST.get('username', None)
    deleted = geouser.del_following(request, userid=userid, username=username)
    return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")

#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
@ajax_request
def get_timeline(request):
    '''
        Devuelve la lista de timeline de un usuario.
        Si no se especifica userid o username, se devuelve el timeline completo del usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    ''' 
    userid = request.POST.get('id', None)
    username = request.POST.get('username', None)
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    timeline = geouser.get_timeline(request, userid, username, page=page, query_id=query_id)
    return HttpResponse(simplejson.dumps(timeline), mimetype="application/json")

@ajax_request
def get_chronology(request):
    '''
        Devuelve la lista de timeline de los followings del usuario logueado.
        Parametros en POST
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    ''' 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    chronology = geouser.get_chronology(request, page=page, query_id=query_id)
    return HttpResponse(simplejson.dumps(chronology), mimetype="application/json")
    

#===============================================================================
# FUNCIONES PARA LISTAS
#===============================================================================
@ajax_request
def get_list_id(request):
    '''
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    '''
    list_id = request.POST.get('list_id', None)
    list = geolist.get_list_id(request, list_id)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def get_list_user(request):
    '''
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    '''
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    if list_id is not None:
        list = geolist.get_list_user_id(request, list_id)
    elif list_name is not None and list_name != '':
        list = geolist.get_list_user_name(request, list_name)
    else:
        list = None
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def get_list_alert(request):
    '''
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    '''
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    if list_id is not None:
        list = geolist.get_list_alert_id(request, list_id)
    elif list_name is not None and list_name != '':
        list = geolist.get_list_alert_name(request, list_name)
    else:
        list = None
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def new_list_user(request):
    '''
    Crea una nueva lista de usuarios
    Parametros en POST    
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de usuarios iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    '''
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.add_list_user(request, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def new_list_alert(request):
    '''
    Crea una nueva lista de alertas
    Parametros en POST    
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de usuarios iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    '''
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.add_list_alert(request, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def mod_list_user(request):
    '''
    Modifica una lista de usuarios
    Parametros en POST    
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
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.mod_list_user(request, id = list_id, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def mod_list_alert(request):
    '''
    Modifica una lista de alertas
    Parametros en POST    
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
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.mod_list_alert(request, id = list_id, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def del_list(request):
    '''
    Borra una lista
    Parametros POST
        :param id: identificador de la lista
        :type id: :class:`integer`
        
        :returns: True si se borro la lista
    '''
    list_id = request.POST.get('list_id', None)
    list = geolist.del_list(request, id = list_id)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def get_all_list_user(request):
    '''
    Obtiene las listas de usuario de un usuario
    Parametros POST
        :param id: identificador de la lista
        :type id: :class:`integer`
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    '''
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_user(request, page = page, query_id = query_id)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")

@ajax_request
def get_all_list_alert(request):
    '''
    Obtiene las listas de alertas de un usuario
    Parametros POST
        :param id: identificador de la lista
        :type id: :class:`integer`
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    '''
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_alert(request, page = page, query_id = query_id)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")

@ajax_request
def get_all_list_suggestion(request):
    '''
    Obtiene las listas de sugerencias de un usuario
    Parametros POST
        :param id: identificador de la lista
        :type id: :class:`integer`
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    '''
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_suggestion(request, query_id=query_id, page=page)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")
    
    