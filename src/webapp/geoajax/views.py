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
import geovote.views as geovote

"""
.. module:: views
    :platform: appengine
    :synopsis: Views for AJAX request
"""
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


@ajax_request
def exists(request):
    """
        Comprueba que un email esta en uso
        Parametros POST:
            email: email a buscar
    """
    if not request.POST.get('email'):
        return HttpResponseBadRequest()
    user = User.objects.get_by_email( request.POST.get('email') )
    if user:
        return HttpResponse('{"result":"exists"}',mimetype="application/json")
    else:
        return HttpResponse('{"result":""}',mimetype="application/json")


@ajax_request
def register(request):
    """
        Realiza el registro de un usuario
        Por POST debe llevar los campos del formulario 'geouser.forms.RegisterForm'
        
        :returns: dict con error y _redirect
    """
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
    """
        Inicia sesion con un usuario
        Por POST debe llevar los campos del formulario 'geouser.forms.LoginForm'
        
        :returns: dict con error y _redirect
    """
    from geouser.views import login
    data = {}
    data['error'], data['_redirect'] = login(request)
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


#===============================================================================
# FUNCIONES AJAX PARA OBTENER, MODIFICAR, BORRAR ALERTAS
#===============================================================================
@ajax_request
def add_reminder(request):
    """
        Añade o edita una alerta
        Parametros en POST:
            eventid: el id del evento a editar (opcional)
            address: direccion
    """
    form = RemindForm(request.POST)
    address = request.POST.get('address', None)
    if form.is_valid():
        eventid = request.POST.get('eventid', None)
        if eventid:
            alert = geoalert.edit_alert(request, eventid, form, address)
        else: 
            alert = geoalert.add_alert(request, form, address=address)
        return HttpResponse(simplejson.dumps(dict(id=alert.id)), mimetype="application/json")
    else:
        return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")

@ajax_request
def get_reminder(request):
    """
        Obtiene los eventos
        Parametros en POST:
            eventid: el id del evento a buscar
            done: si solo se quieren los eventos realizados (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
    """
    eventid = request.POST.get('eventid', None)
    done = request.POST.get('done', None)
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    alerts = geoalert.get_alert(request, eventid, done, page, query_id)
    return HttpResponse(getAlertsJSON(alerts), mimetype="application/json")

@ajax_request
def delete_reminder(request):
    """
        Borra un evento
        Parametros en POST
            eventid : el id de la alerta a borrar
    """
    eventid = request.POST.get('eventid', None)
    geoalert.del_alert(request, eventid)    
    return HttpResponse()

#===============================================================================
# FUNCIONES AJAX PARA OBTENER, MODIFICAR, BORRAR SUGERE
#===============================================================================
def add_suggestion(request):
    """
        Añade o edita una alerta
        Parametros en POST:
            eventid: el id del evento a editar (opcional)
    """
    form = SuggestionForm(request.POST)
    if form.is_valid():
        eventid = request.POST.get('eventid', None)
        if eventid:
            sug = geoalert.edit_suggestion(request, eventid, form)
        else: 
            sug = geoalert.add_suggestion(request, form)
        return HttpResponse(simplejson.dumps(dict(id=sug.id)), mimetype="application/json")
    else:
        return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")


def add_suggestion_invitation(request):
    """
        Envia una invitacion a un usuario
        Parametros en POST:
            eventid: el id del evento a donde invitar al usuario
            userid: el id del usuario a invitar
    """
    userid = request.POST.get('userid')
    eventid = request.POST.get('eventid')
    invitation = geoalert.add_suggestion_invitation(request, eventid, userid)
    return HttpResponse(simplejson.dumps(invitation), mimetype="application/json")

def add_suggestion_follower(request):
    eventid = request.POST.get('eventid')
    result = geoalert.add_suggestion_follower(request, eventid)
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@ajax_request
def get_suggestion(request):
    """
        Obtiene los eventos
        Parametros en POST:
            eventid: el id del evento a buscar (opcional)
            wanted_user: usuario a buscar (opcional, por defecto, es uno mismo)
            private_profile: busqueda para mostrar en el perfil privado del usuario
            query_id: id de la consulta de pagina
            page : pagina a mostrar
    """
    eventid = request.POST.get('eventid', None)
    wanted_user = request.POST.get('wanteduser', request.user)
    private_profile= str2bool(request.POST.get('private_profile', ''))
    if private_profile and wanted_user != request.user:
        raise AttributeError
    query_id = request.POST.get('query_id', None)
    page = int(request.POST.get('page', 1))
    suggestions = geoalert.get_suggestion(request, eventid, wanted_user, private_profile, page, query_id)
    return HttpResponse(getAlertsJSON(suggestions), mimetype="application/json")

@ajax_request
def delete_suggestion(request):
    """
        Borra un evento
        Parametros en POST
            eventid : el id de la sugerencia a borrar
    """
    eventid = request.POST.get('eventid', None)
    deleted = geoalert.del_suggestion(request, eventid)
    return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")


#===============================================================================
# FUNCIONES AJAX PARA OBTENER FOLLOWERS Y FOLLOWINGS
#===============================================================================
@ajax_request
def get_followers(request):
    """
        Devuelve la lista de followers de un usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma (id, username)
    """ 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    followers = geouser.get_followers(request, userid, username, page, query_id)
    return HttpResponse(simplejson.dumps(followers), mimetype="application/json")  # los None se parsean como null

@ajax_request
def get_followings(request):
    """
        Devuelve la lista de followings de un usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma (id, username)
    """ 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    followings = geouser.get_followings(request, userid, username, page, query_id)
    return HttpResponse(simplejson.dumps(followings), mimetype="application/json")

@ajax_request
def get_friends(request):
    """
    Devuelve una lista con los usuarios que siguen y sigue el usuario
    
        :returns: lista de la forma (id, username)
    """
    friends = geouser.get_friends(request)
    return HttpResponse(simplejson.dumps(friends), mimetype="application/json")

@ajax_request
def add_following(request):
    """
        Añade a la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
       
            :returns: boolean
    """ 
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    if username == 'None':
        username=None
    added = geouser.add_following(request, userid=userid, username=username)
    return HttpResponse(simplejson.dumps(added), mimetype="application/json")
    
@ajax_request
def delete_following(request):
    """
        Borra de la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a borrar
            username : el username del usuario a borrar
       
            :returns: boolean
    """
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    deleted = geouser.del_following(request, userid=userid, username=username)
    return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")

@ajax_request
def get_contacts_google(request):
    return geouser.get_perms_google(request)

@ajax_request
def get_friends_facebook(request):
    friends = geouser.get_friends_facebook(request)
    return HttpResponse(simplejson.dumps(friends))

@ajax_request
def get_friends_twitter(request):
    friends = geouser.get_friends_twitter(request)
    return HttpResponse(simplejson.dumps(friends))

#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
@ajax_request
def get_timeline(request):
    """
        Devuelve la lista de timeline de un usuario.
        Si no se especifica userid o username, se devuelve el timeline completo del usuario
        Parametros en POST
            userid : el id del usuario a buscar (opcional)
            username : el username del usuario a buscar (opcional)
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    """ 
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    timeline = geouser.get_timeline(request, userid, username, page=page, query_id=query_id)
    return HttpResponse(simplejson.dumps(timeline), mimetype="application/json")

@ajax_request
def get_chronology(request):
    """
        Devuelve la lista de timeline de los followings del usuario logueado.
        Parametros en POST
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    """ 
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    chronology = geouser.get_chronology(request, page=page, query_id=query_id)
    return HttpResponse(simplejson.dumps(chronology), mimetype="application/json")
    

#===============================================================================
# FUNCIONES PARA LISTAS
#===============================================================================
@ajax_request
def get_list_id(request):
    """
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    """
    list_id = request.POST.get('list_id', None)
    list = geolist.get_list_id(request, list_id)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def get_list_user(request):
    """
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    """
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
    """
    Devuelve la lista buscada por ID
    Parametros en POST
        list_id : lista a buscar
        
        :returns: (list_id, list_name, list_description, list_created
    """
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
    """
    Crea una nueva lista de usuarios
    Parametros en POST    
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de usuarios iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    """
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.add_list_user(request, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def new_list_alert(request):
    """
    Crea una nueva lista de alertas
    Parametros en POST    
        :param name: nombre para la lista (el nombre es unico)
        :type name: :class:`string`
        :param description: descripcion de la lista (opcional)
        :type description: :class:`string`
        :param instances: lista de usuarios iniciales (opcional)
        :type instances: :class:`list`
        :returns: id de la lista creada o modificada si ya existia
    """
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.add_list_alert(request, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def mod_list_user(request):
    """
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
    """
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.mod_list_user(request, id = list_id, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def mod_list_alert(request):
    """
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
    """
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('list_name', None)
    list_description = request.POST.get('list_description', None)
    list_instances = request.POST.get('list_instances', [])
    
    list = geolist.mod_list_alert(request, id = list_id, name = list_name, description = list_description, instances = list_instances)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def delete_list(request):
    """
    Borra una lista
    Parametros POST
        :param list_id: identificador de la lista
        :type list_id: :class:`integer`
        
        :returns: True si se borro la lista
    """
    list_id = request.POST.get('list_id', None)
    list = geolist.del_list(request, id = list_id)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")

@ajax_request
def get_all_list_user(request):
    """
    Obtiene las listas de usuario de un usuario
    Parametros POST
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_user(request, page = page, query_id = query_id)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")

@ajax_request
def get_all_list_alert(request):
    """
    Obtiene las listas de alertas de un usuario
    Parametros POST
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_alert(request, page = page, query_id = query_id)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")

@ajax_request
def get_all_list_suggestion(request):
    """
    Obtiene las listas de sugerencias de un usuario
    Parametros POST
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_list_suggestion(request, query_id=query_id, page=page)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json")
    
@ajax_request
def get_all_public_list_suggestion(request):
    """
    Obtiene todas las listas de sugerencias publicas
    Parametros POST
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    lists = geolist.get_all_public_list_suggestion(request, query_id=query_id, page=page)
    
    return HttpResponse(getListsJSON(lists), mimetype="application/json") 

@ajax_request
def get_all_shared_list_suggestion(request):
    """
    Obtiene todas las lista de sugerencias para las que
    el usuario tiene invitacion
    """
    lists = geolist.get_all_shared_list_suggestion(request)
    
    return HttpResponse(simplejson.dumps(lists), mimetype="application/json")

#===============================================================================
# COMENTARIOS Y VOTOS
#===============================================================================
@ajax_request
def delete_comment(request):
    """
    Borra un comentario
    Parametros POST:
        commentid: id del comentario a borrar
    """
    commentid = request.POST['comment_id']
    comment = geovote.delete_comment(request, commentid)
    return HttpResponse(simplejson.dumps(comment), mimetype="application/json")

@ajax_request
def do_comment_event(request):
    """
    Realiza un comentario a un evento (alerta, sugerencia, etc.)
    Parametros POST
        instance_id: evento a comentar
        msg: mensaje
    """
    instance_id = request.POST['instance_id']
    msg = request.POST['msg']
    comment = geovote.do_comment_event(request, instance_id, msg)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(comment, cls=JSONEncoder),
                        mimetype="application/json")
    
@ajax_request
def get_comments_event(request):
    """
    Obtiene todas los comentarios visibles de un evento
    Parametros POST
        instance_id: evento a mostrar
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    instance_id = request.POST['instance_id']
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    comments = geovote.get_comments_event(request, instance_id, query_id, page) 
    
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(comments, cls=JSONEncoder),
                        mimetype="application/json")

@ajax_request
def do_comment_list(request):
    """
    Realiza un comentario a una lista
    Parametros POST
        instance_id: lista a comentar
        msg: mensaje
    """
    instance_id = request.POST['instance_id']
    msg = request.POST['msg']
    comment = geovote.do_comment_list(request, instance_id, msg),
    
    return HttpResponse(simplejson.dumps(comment),
                        mimetype="application/json")

@ajax_request
def get_comments_list(request):
    """
    Obtiene todas los comentarios visibles de una lista
    Parametros POST
        instance_id: lista a mostrar
        page: pagina a mostrar
        query_id: id de la consulta de pagina
    """
    instance_id = request.POST['instance_id']
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    comments = geovote.get_comments_list(request, instance_id, query_id, page) 
    
    return HttpResponse(simplejson.dumps(comments),
                        mimetype="application/json")

@ajax_request
def do_vote_suggestion(request):
    """
    Vota una sugerencia
    Parametros POST
        instance_id: sugerencia a votar
        puntuation: puntuacion a añadir
    """
    instance_id = request.POST['instance_id']
    puntuation = request.POST['puntuation']
    
    vote = geovote.do_vote_suggestion(request, instance_id, puntuation)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")
    
@ajax_request
def do_vote_list(request):
    """
    Vota una lista
    Parametros POST
        instance_id: lista a votar
        puntuation: puntuacion a añadir
    """
    instance_id = request.POST['instance_id']
    puntuation = request.POST['puntuation']
    vote = geovote.do_vote_list(request, instance_id, puntuation)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")
    
@ajax_request
def do_vote_comment(request):
    """
    Vota un comentario
    Parametros POST
        instance_id: comentario
        puntuation: puntuacion a añadir
    """
    instance_id = request.POST['instance_id']
    puntuation = request.POST['puntuation']
    vote = geovote.do_vote_comment(request, instance_id, puntuation)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")
    
@ajax_request
def get_vote_suggestion(request):
    """
    Obtiene el contador de votos de una sugerencia
    Parametros POST
        instance_id: sugerencia a mostrar
    """
    instance_id = request.POST['instance_id']
    vote = geovote.get_vote_suggestion(request, instance_id) 
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")

@ajax_request
def get_vote_list(request):
    """
    Obtiene el contador de votos de una lista
    Parametros POST
        instance_id: sugerencia a mostrar
    """
    instance_id = request.POST['instance_id']
    vote = geovote.get_vote_list(request, instance_id) 
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")

@ajax_request
def get_vote_comment(request):
    """
    Obtiene el contador de votos de un comentario
    Parametros POST
        instance_id: sugerencia a mostrar
    """
    instance_id = request.POST['instance_id']
    vote = geovote.get_vote_comment(request, instance_id) 
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder), 
                        mimetype="application/json")

@ajax_request
def mod_searchconfig_google(request):
    sconfig = request.user.settings.searchconfig_google
    sconfig.region_code = request.POST['region_code']
    sconfig.location = db.GeoPt(request.POST['location'])
    sconfig.radius = int(request.POST['radius'])
    sconfig.type = request.POST['type']
    sconfig.put()
    return HttpResponse()


@ajax_request
def get_place_near(request):
    """
    Obtiene places cercanos a una localizacion dada
    Parametros POST:
        location: punto donde buscar
        radius: radio para las busquedas, en metros (opcional)
        
        return 
    """
    location = request.POST['location']
    radius = request.POST.get('radius', 2000)
    from geoalert.models_poi import Place
    places = Place.objects.get_nearest(location, radius)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(places, cls=JSONEncoder),
                        mimetype='application/json')