# coding=utf-8


from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
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
def add_suggestion(request):
    """
        Añade o edita una alerta
        Parametros en POST:
            eventid: el id del evento a editar (opcional)
    """
    form = SuggestionForm(request.POST)
    if form.is_valid():
        eventid = request.POST.get('eventid', None)
        sug = geoalert.save_suggestion(request, form, id=eventid)
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
    username = request.POST.get('username')
    eventid = request.POST.get('eventid')
    invitation = geoalert.add_suggestion_invitation(request, eventid, username)
    return HttpResponse(simplejson.dumps(invitation), mimetype="application/json")


def add_suggestion_follower(request):
    eventid = request.POST.get('eventid')
    result = geoalert.add_suggestion_follower(request, eventid)
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


def delete_suggestion_follower(request):
    eventid = request.POST.get('eventid')
    result = geoalert.del_suggestion_follower(request, eventid)
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
        query_id = request.POST.get('query_id', None)
        if query_id is not None:
            query_id = query_id.split('_')
            sug_id = query_id[0]
            foll_id = query_id[1]
        else:
            sug_id = None
            foll_id = None
        page = int(request.POST.get('page', 1))
        suggestions = geoalert.get_suggestion(request, id=eventid, wanted_user=wanted_user, page=page, query_id=sug_id)
        suggestions_following = geoalert.get_suggestion_following(request, page=page, query_id=foll_id)
        suggestions[1].extend(suggestions_following[1]).sort(key=lambda x: x.modified, reverse=True)
        suggestions[1].sort(key=lambda x: x.modified, reverse=True)
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
    userid = request.POST.get('userid', None)
    username = request.POST.get('username', None)
    if username == 'None':
        username=None
    added = geouser.add_following(request.user, userid=userid, username=username)
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
    deleted = geouser.del_following(request.user, userid=userid, username=username)
    return HttpResponse(simplejson.dumps(deleted), mimetype="application/json")


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
            return HttpResponse(simplejson.dumps(True))
    return HttpResponse(simplejson.dumps(True))


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
    list_id = request.POST.get('list_id', None)
    list_name = request.POST.get('name', None)
    list_description = request.POST.get('description', None)
    list_instances = request.POST.getlist('suggestions[]')
    list_instances_del = request.POST.getlist('suggestions_del[]')
    list_vis = request.POST.get('visibility', None)
    if not 'tags' in request.POST:
        list_tags = None
    else:
        list_tags = request.POST.getlist('tags')
    list = geolist.add_list_suggestion(request, id=list_id, name = list_name,
                                 description = list_description,
                                 instances = list_instances,
                                 instances_del = list_instances_del,
                                 tags=list_tags,
                                 vis=list_vis
                                 )
    if list is False:
        return HttpResponseForbidden()
    if list is not None:
        return HttpResponse(list.to_json(), mimetype="application/json")
    return HttpResponse(list, mimetype="application/json")


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
        
        return 
    """
    
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    location = request.POST.get('location', None)
    if location is not None:
        from google.appengine.ext import db
        request.user.last_location = db.GeoPt(location)
    else:
        location = request.user.last_location
    radius = request.POST.get('radius', 5000)
    from geoalert.models import Suggestion
    suggs = Suggestion.objects.get_nearest(location, radius)
    from libs.jsonrpc.jsonencoder import JSONEncoder
    return HttpResponse(simplejson.dumps(suggs, cls=JSONEncoder),
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
    return HttpResponse(simplejson.dumps(response, cls=JSONEncoder),
                        mimetype='application/json')
    
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
