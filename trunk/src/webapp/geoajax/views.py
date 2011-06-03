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

from funcs import getAlertsJSON
from decorators import ajax_request
from geouser.models import User
import geouser.views as geouser
from geouser.funcs import init_user_session, login_func
from geoalert.forms import *
from geoalert.models import *
import geoalert.views as geoalert


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
    return HttpResponse(simplejson(followers), mimetype="application/json")  # los None se parsean como null

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
    return HttpResponse(simplejson(added), mimetype="application/json")
    
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
    return HttpResponse(simplejson(deleted), mimetype="application/json")

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
    

    

