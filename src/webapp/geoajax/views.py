# coding=utf-8


from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from decorators import ajax_request
from geouser.models import User
import geouser.api as geouser
from geouser.funcs import login_func
from geoalert.forms import RemindForm, SuggestionForm
import geoalert.views as geoalert
import geolist.views as geolist
import geovote.api as geovote

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
    from funcs import getAlertsJSON
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
def save_suggestion(request):
    """
        Añade o edita una sugerencia
        Parametros en POST:
            eventid: el id del evento a editar (opcional)
    """
    form = SuggestionForm(request.POST)
    if form.is_valid():
        eventid = request.POST.get('eventid', None)
        sug = geoalert.save_suggestion(request, form, id=eventid)
        if isinstance(sug, HttpResponse):
            return sug
        return HttpResponse(simplejson.dumps(dict(id=sug.id)), mimetype="application/json")
    return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")


def add_suggestion_invitation(request):
    """
        Envia una invitacion a un usuario
        Parametros en POST:
            eventid: el id del evento a donde invitar al usuario
            userid: el id del usuario a invitar
    """
    username = request.POST.get('username')
    eventid = request.POST.get('eventid')
    invitation = geoalert.add_suggestion_invitation(request, eventid, username)
    if isinstance(invitation, HttpResponse):
        return invitation
    return HttpResponse(simplejson.dumps(invitation), mimetype="application/json")


def add_suggestion_follower(request):
    eventid = request.POST.get('eventid')
    result = geoalert.add_suggestion_follower(request, eventid)
    if isinstance(result, HttpResponse):
        return result
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def delete_suggestion_follower(request):
    eventid = request.POST.get('eventid')
    result = geoalert.del_suggestion_follower(request, eventid)
    if isinstance(result, HttpResponse):
        return result
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
    if eventid is None:
        from geoalert.api import get_suggestions_dict
        suggestions = get_suggestions_dict(wanted_user) # FIXME: devolver solo publicas
    else:
        suggestions = geoalert.get_suggestion(request, id=eventid, wanted_user=wanted_user)    
    from funcs import getAlertsJSON
    return HttpResponse(getAlertsJSON(suggestions), mimetype="application/json")


@ajax_request
def get_suggestion_following(request):
    query_id = request.POST.get('query_id', None)
    page = int(request.POST.get('page', 1))
    suggestions = geoalert.get_suggestion_following(request, page=page, query_id=query_id)
    from funcs import getAlertsJSON
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
    try:
        return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")
    except:
        return HttpResponseNotFound()


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
    followers = geouser.get_followers(request.user, userid, username, page, query_id)
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
    followings = geouser.get_followings(request.user, userid, username, page, query_id)
    return HttpResponse(simplejson.dumps(followings), mimetype="application/json")


@ajax_request
def add_following(request):
    """
        Añade a la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a seguir
            username : el username del usuario a seguir
       
            :returns: boolean
    """ 
    from django.conf import settings
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    if username == 'None':
        username=None
    added = geouser.add_following(request.user, userid=userid, username=username)
    if not isinstance(added, HttpResponse):
        return HttpResponse(simplejson.dumps(added), mimetype="application/json")
    return added

    
@ajax_request
def delete_following(request):
    """
        Borra de la lista de de followings de un usuario
        Parametros en POST
            userid : el id del usuario a borrar
            username : el username del usuario a borrar
       
            :returns: boolean
    """
    from django.conf import settings
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    deleted = geouser.del_following(request.user, userid=userid, username=username)
    if not isinstance(deleted, HttpResponse):
        return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")
    return deleted


@ajax_request
def block_contacts(request):
    """
        Bloquea a un usuario para no recibirlo en la lista
        de amigos sugeridos
        
        Parametros en POST:
            userid: el id del usuario a bloquear
            
            :returns: boolean
    """
    if request.user.is_authenticated():
        userid = int(request.POST['userid'])
        if userid is not None:
            import memcache
            request.user.settings.blocked_friends_sug.append(userid)
            friends = memcache.get('%sfriends_to_%s' % (memcache.version, request.user.key()))
            if friends is not None and userid in friends:
                del friends[userid]
                memcache.set('%sfriends_to_%s' % (memcache.version, request.user.key()), friends, 300)
            request.user.settings.put()
            return HttpResponse(simplejson.dumps(True), mimetype="application/json")
    return HttpResponse(simplejson.dumps(True), mimetype="application/json")


@ajax_request
def get_contacts(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    handlers_rpcs, list_rpc=request.user.get_friends_to_follow(rpc=True)
    friends = request.user._callback_get_friends_to_follow(handlers_rpcs, list_rpc)
    from geouser.models_acc import UserCounter
    from georemindme.funcs import fetch_parentsKeys
    top_users = UserCounter.all(keys_only=True).order('-suggested').fetch(5)
    top_users = fetch_parentsKeys(top_users)
    top_users = filter(None, top_users)
    for user in top_users:
        if not user.key() == request.user.key() and not request.user.is_following(user):
            friends[user.id] = {'username': user.username,
                                'id': user.id
                                }
    friends_to_list = friends.values()
    return HttpResponse(simplejson.dumps(friends_to_list), mimetype="application/json")


#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
@ajax_request
def get_profile_timeline(request):
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
    query_id = request.POST.get('query_id', None)
    timeline = geouser.get_profile_timeline(request.user, userid, username, query_id=query_id)
    from funcs import render_timeline
    if timeline is not None:
        timeline[1] = render_timeline(request, timeline[1])
    return HttpResponse(simplejson.dumps(timeline), mimetype="application/json")


@ajax_request
def get_activity_timeline(request):
    """
        Devuelve la lista de timeline de los followings del usuario logueado.
        Parametros en POST
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    """ 
    query_id = list(request.POST.getlist('query_id'))
    query_id = simplejson.loads(query_id[0])
    activity = geouser.get_activity_timeline(request.user, query_id=query_id)
    from funcs import render_timeline
    activity[1] = render_timeline(request, activity[1])
    return HttpResponse(simplejson.dumps(activity), mimetype="application/json")


@ajax_request
def get_notifications_timeline(request):
    """
        Devuelve la lista de timeline de los followings del usuario logueado.
        Parametros en POST
            page : pagina a mostrar
            query_id: id de la consulta de pagina
        
        :returns: lista de la forma [query_id, [(id, username, avatar)]]
    """ 
    query_id = request.POST.get('query_id', None)
    chronology = geouser.get_notifications_timeline(request.user, query_id=query_id)
    from funcs import render_timeline
    chronology[1] = render_timeline(request, chronology[1])
    return HttpResponse(simplejson.dumps(chronology), mimetype="application/json")
    

#===============================================================================
# FUNCIONES PARA LISTAS
#===============================================================================
@ajax_request
def delete_list(request):
    """
    Borra una lista de sugerencias
    Parametros en POST:
        list_id: id de la lista
    """
    list_id = request.POST.get('list_id', None)
    list = geolist.del_list(request, id = list_id)
    return HttpResponse(simplejson.dumps(list), mimetype="application/json")


@ajax_request
def get_list_suggestion(request):
    """
    Devuelve todas las listas de sugerencias
    si no se especifica id
    Parametros en POST:
        list_id: id de la lista (opcional)
        user_id: id del usuario del que buscar listas (opcional,
            si no se especifica se busca del usuario identificado)
            
    """
    list_id = request.POST.get('list_id', None)
    user_id = request.POST.get('user_id', None)
    page = request.POST.get('page', 1)
    query_id = request.POST.get('query_id', None)
    lists = geolist.get_list_suggestion(request, list_id=list_id, user_id=user_id, query_id=query_id, page=page)
    from funcs import getListsJSON
    return HttpResponse(getListsJSON(lists), mimetype="application/json")


@ajax_request
def add_list_suggestion(request):
    """
    Cra una lista de sugerencias o modifica una
    si se especifica id
    Parametros en POST:
        list_id: id de la lista (opcional)
        name: nombre de la lista (unico por usuario)
        description: descripcion (opcional)
        suggestions: lista de ids de sugerencias    
    """
    list_id = request.POST.getlist('list_id[]')
    list_name = request.POST.get('name', None)
    list_description = request.POST.get('description', None)
    list_instances = request.POST.getlist('suggestions[]')
    list_instances_del = request.POST.getlist('suggestions_del[]')
    list_vis = request.POST.get('visibility', None)
    if not 'tags' in request.POST:
        list_tags = None
    else:
        list_tags = request.POST.getlist('tags')
    try:
        lists = geolist.add_list_suggestion(request, lists_id=list_id, name = list_name,
                                     description = list_description,
                                     instances = list_instances,
                                     instances_del = list_instances_del,
                                     tags=list_tags,
                                     vis=list_vis
                                     )
    except:
        return HttpResponseBadRequest()
    return HttpResponse([list.to_json() if hasattr(list, 'to_json') else None for list in lists], mimetype="application/json")


@ajax_request
def add_suggestion_list_invitation(request):
    """
        Envia una invitacion a un usuario
        Parametros en POST:
            eventid: el id del evento a donde invitar al usuario
            userid: el id del usuario a invitar
    """
    username = request.POST.get('username')
    eventid = request.POST.get('list_id')
    invitation = geolist.add_suggestion_list_invitation(request, eventid, username)
    return HttpResponse(simplejson.dumps(invitation), mimetype="application/json")


@ajax_request
def add_list_follower(request):
    list_id = request.POST.get('list_id')
    added = geolist.add_list_follower(request, list_id)
    return HttpResponse(simplejson.dumps(added), mimetype="application/json")


def delete_list_follower(request):
    list_id = request.POST.get('list_id')
    result = geolist.del_list_follower(request, list_id)
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")
    
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
    comment = geovote.delete_comment(request.user, commentid)
    return HttpResponse(simplejson.dumps(comment), mimetype="application/json")

@ajax_request
def do_comment(request, kind):
    """
    Realiza un comentario a un evento (alerta, sugerencia, etc.)
    Parametros POST
        instance_id: evento a comentar
        msg: mensaje
    """
    instance_id = request.POST['instance_id']
    msg = request.POST['msg']
    comment = geovote.do_comment(request.user, instance_id, kind, msg)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(comment, cls=JSONEncoder),
                        mimetype="application/json")
    

@ajax_request
def get_comments(request, kind):
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
    comments = geovote.get_comments(request.user, instance_id, kind, query_id, page) 
    
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(comments, cls=JSONEncoder),
                        mimetype="application/json")


@ajax_request
def do_vote(request, **kwargs):
    """
    Vota una sugerencia
    Parametros POST
        instance_id: sugerencia a votar
        puntuation: puntuacion a añadir
    """
    instance_id = request.POST['instance_id']
    puntuation = request.POST.get('puntuation', 1)
    
    vote = geovote.do_vote(request.user, kwargs['kind'], instance_id, puntuation)
    if vote is None:
        from django.shortcuts import Http404
        raise Http404
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(vote, cls=JSONEncoder),
                        mimetype="application/json")
    

@ajax_request
def mod_searchconfig_google(request):
    from google.appengine.ext.db import GeoPt
    sconfig = request.user.settings.searchconfig_google
    sconfig.region_code = request.POST['region_code']
    sconfig.location = GeoPt(request.POST['location'])
    sconfig.radius = int(request.POST['radius'])
    sconfig.type = request.POST['type']
    sconfig.put()
    return HttpResponse()


@ajax_request
def get_near_places(request):
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
    
@ajax_request
def get_near_suggestions(request):
    """
    Obtiene places cercanos a una localizacion dada
    Parametros POST:
        location: punto donde buscar
        radius: radio para las busquedas, en metros (opcional)
        
        return suggestion list
    """
    
    location = request.POST.get('location', None)
    if location is None and not request.user.is_authenticated():
        return HttpResponseForbidden()
    if location is not None and request.user.is_authenticated():
        from google.appengine.ext import db
        request.user.last_point = db.GeoPt(location)
        try:
            from mapsServices.maps import MapsRequest
            result = MapsRequest()
            result = result.get_address(request.user.last_point)
            if 'formatted_address' in result['results'][0]:
                request.user.last_adress = result['results'][0]['formatted_address']
        except:
            pass
        request.user.put()
    if location is None and request.user.is_authenticated():
        location = request.user.last_point
    radius = request.POST.get('radius', 5000)
    try:
        limit = int(request.POST.get('limit', 4))
    except:
        return HttpResponseBadRequest()
    from geoalert.models import Suggestion
    suggs = Suggestion.objects.get_nearest(location, radius, querier=request.user)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(suggs[:limit], cls=JSONEncoder),
                        mimetype='application/json')
    
@ajax_request
def search_tag_suggestion(request):
    tag = request.POST.get('tag', None)
    query_id = request.POST.get('query_id', None)
    page = request.POST.get('page', 1)
    if tag is None:
        return HttpResponseBadRequest
    from geotags.views import search_tag_suggestion
    response = search_tag_suggestion(request, tag, page=page, query_id=query_id)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    try:
        return HttpResponse(simplejson.dumps(response, cls=JSONEncoder),
                            mimetype='application/json')
    except:
        return response
    
@ajax_request
def add_suggestion_tags(request):
    tags = request.POST.get('tags', None)
    event_id = request.POST.get('event_id', None)
    if tags is None or event_id is None:
        return HttpResponseBadRequest
    from geotags.views import add_suggestion_tag
    response = add_suggestion_tag(request, event_id, tags)
    if not response:
        return HttpResponseBadRequest
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(response, cls=JSONEncoder),
                        mimetype='application/json')
    

@ajax_request
def get_short_url(request):
    url = request.POST.get('url', None)
    from libs.vavag import VavagRequest, VavagException
    try:
        from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global
        client = VavagRequest(__web_settings.SHORTENER_ACCESS['user'], __web_settings.SHORTENER_ACCESS['key'])
        response =  client.set_pack(url)
        return HttpResponse(simplejson.dumps(response['results']['packUrl']),
                            mimetype='application/json')
    except VavagException, e:
        return HttpResponseBadRequest(simplejson.dumps(e.msg),
                                      mimetype='application/json')
    except:
        return HttpResponseBadRequest()


@ajax_request
def share_on_facebook(request):
    response = None
    event_id = request.POST.get('event_id', None)
    msg = request.POST.get('msg', None)
    if event_id is not None:
        response = geoalert.share_on_facebook(request, event_id, msg)
    else:
        list_id =request.POST.get('list_id', None)
        response = geolist.share_on_facebook(request, list_id, msg)
    if response is not None:
        return HttpResponse(simplejson.dumps(response),
                            mimetype='application/json')
    return HttpResponseBadRequest()


@ajax_request
def share_on_twitter(request):
    response = None
    event_id = request.POST.get('event_id', None)
    msg = request.POST.get('msg', None)
    if event_id is not None:
        response = geoalert.share_on_twitter(request, event_id, msg)
    else:
        list_id =request.POST.get('list_id', None)
        response = geolist.share_on_twitter(request, list_id, msg)
    if response is not None:
        return HttpResponse(simplejson.dumps(response),
                            mimetype='application/json')
    return HttpResponseBadRequest()


@ajax_request
def suggested_list_suggestion(request):
    """
        si se envia timeline_id por POST, se modificara ese timeline (se aceptara o rechazara la sugerencia)
        status puede ser 0: nada 1: aceptada, 2: rechazada
        si no se envia timeline_id, debe enviarse list_id y event_id para hacer la peticion
        
        devuelve True si todo fue correcto, False si ya existe la sugerencia o no se puede enviar, None si la lista o la 
        sugerencia no existen
    """
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    timeline_id = request.POST.get('timeline_id', None)
    if timeline_id is None:
        list_id = request.POST.get('list_id', None)
        event_id = request.POST.get('event_id', None)
        if list_id is not None and event_id is not None:
            from geoalert.api import send_suggestion_to_list
            added = send_suggestion_to_list(request.user, list_id, event_id)
            return HttpResponse(simplejson.dumps(added),
                            mimetype='application/json') 
        else:
            return HttpResponseBadRequest()
    try:
        timeline_id = int(timeline_id)
        status = int(request.POST.get('status', 0))
        from geoalert.api import change_suggestion_to_list
        changed = change_suggestion_to_list(request.user, timeline_id, status)
        return HttpResponse(simplejson.dumps(changed),
                                mimetype='application/json')
    except:
        raise
        return HttpResponseBadRequest()
    
    
    
@ajax_request
def get_suggestions(request):
    from geoalert import api
    list_id = request.POST.get('list_id', None)
    suggs = api.get_suggestions_dict(request.user, list_id=list_id)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps([{'id': s.key().id(),
                                          'name': s['name'],
                                          'description': s['description'],
                                          'created': s['created'],
                                          'lists': api.get_list_from_suggs(s, request.user), 
                                         } for s in suggs],
                                         cls=JSONEncoder
                                         ), mimetype='application/json')
    
@ajax_request
def get_perms(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden
    from google.appengine.ext import db
    perms = {'facebook': False,
             'twitter': False,
             'google': False,
             }
    from geouser.models_social import SocialUser
    facebook = db.GqlQuery("SELECT __key__ FROM OAUTH_Access WHERE provider = :provider AND user = :user", provider='facebook', user=request.user.key()).get()
    twitter = db.GqlQuery("SELECT __key__ FROM OAUTH_Access WHERE provider = :provider AND user = :user", provider='twitter', user=request.user.key()).get()
    google = db.GqlQuery("SELECT __key__ FROM OAUTH_Access WHERE provider = :provider AND user = :user", provider='google', user=request.user.key()).get()
    
    if facebook:
        perms['facebook'] = True
    if twitter:
        perms['twitter'] = True
    if google:
        perms['google'] = True
    return HttpResponse(simplejson.dumps(perms), mimetype='application/json')
    
    