# coding=utf-8

"""
.. module:: views
    :platform: appengine
    :synopsis: Servicios ofrecidos al movil
"""


from libs.jsonrpc import jsonrpc_method
from libs.jsonrpc.exceptions import *
try:
    # When deployed
    from google.appengine.runtime import DeadlineExceededError
except ImportError:
    # In the development server
    from google.appengine.runtime.apiproxy_errors import DeadlineExceededError 


def need_authenticate(username=None, password=None):
    """
        No se deja loguearse pasando el nombre y password
        desde cualquier funcion
    """
    raise BadSessionException
    

def parse_date(date, excep=True):
    """
        Parsea la fecha de segundos a un datetime
    """
    if date is None:
        if excep:
            raise InvalidParamsError
        else:
            return None
    if type(date) in (str, unicode,) and not date.isdigit():
        if excep:
            raise InvalidParamsError
        else:
            return None
    from datetime import datetime
    return datetime.fromtimestamp(date)

    
def parse_alertdeleted(deleted, user):
    """
        Borra las alertas recibidas en deleted por el movil
    """
    from geoalert.models import Alert
    for a in deleted:  # borrar las alertas enviadas por el movil
        id = a.get('id', None)
        if id is not None:
            alert = Alert.objects.get_by_id_user(id, user)
            if alert is not None:
                alert.delete()


def parse_listdeleted(deleted, user):
    """
        Borra las listas recibidas en deleted por el movil
    """
    from geolist.models import List
    for a in deleted:  # borrar las alertas enviadas por el movil
        id = a.get('id', None)
        if id is not None:
            list = List.objects.get_by_id_user(id, user)
            if list is not None:
                list.delete()
    

@jsonrpc_method('login', authenticated=False)
def login(request, email, password):
    """
        Logs a user and init a new session, returns the session_id
        if the user is valid
        
            :params email: email del usuario
            :type email: 
    """
    email = unicode(email)
    password = unicode(password)
    from geouser.funcs import login_func
    error, redirect = login_func(request, email=email, password=password, from_rpc=True)
    if error == 0:
        raise NoConfirmedException
    elif error == 1:
        raise InvalidCredentialsError
    elif error != '':
        raise InvalidRequestError         
    return request.session.session_id


@jsonrpc_method('login_facebook', authenticated=False)
def login_facebook(request, access_token):
    """
        Inicia la sesion de un usuario con un token de acceso de facebook
        
        :param access_token: token de acceso valido de facebook
        :type access_token: :class:`string`
        
        :returns: :class:`string` identificador de sesion
    """
    from geoauth.clients.facebook import FacebookClient
    from geouser.funcs import init_user_session
    client = FacebookClient(access_token = access_token)
    user = client.authenticate()
    if not user:
        raise InvalidCredentialsError
    init_user_session(request, user, from_rpc=True)
    return request.session.session_id


@jsonrpc_method('register', authenticated=False)
def register(request, email, password):
    """
        Register a user
        returns True if sucessful
    """
    email = unicode(email)
    password = unicode(password)
    from geouser.models import User
    u = User.register(email=email, password=password)
    if u is not None:
        return True


@jsonrpc_method('sync_alert', authenticated=need_authenticate)
def sync_alert(request, last_sync, modified=[], deleted=[]):
    """
        Sincroniza las alertas
        
        :param last_sync: Ultima fecha de sincronizacion, en epoch
        :type last_sync: :class:`integer`
        :param modified: lista con las alertas modificadas (en diccionario)
        :param deleted: lista con las alertas a borrar (sus ids)
    """
    from geoalert.models import Alert, _Deleted_Alert
    from geoalert.models_poi import PrivatePlace
    
    if type(modified) != type(list()) or type(deleted) != type(list()):
        raise InvalidParamsError
    sync_deleted = []
    temp_alert = {}
    last_sync = parse_date(last_sync)
    parse_alertdeleted(deleted, request.user)
    try:
        from google.appengine.ext.db import GeoPt
        for a in modified:
            id = a.get('id', None)
            if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
                old = Alert.objects.get_by_id_user(id, request.user)
                if not old:  # no existe en la BD, fue borrada.
                    sync_deleted.append({'id': id})
                    continue
                if parse_date(a.get('modified')) <= old.modified:
                    continue
            poi = PrivatePlace.get_or_insert(name = '',
                                             location = GeoPt(a.get('x'), a.get('y')),
                                             address = '',
                                             user = request.user)
            alert = Alert.update_or_insert(
                         id = id,
                         name = a.get('name', u''),
                         description = a.get('description', u''),
                         date_starts = parse_date(a.get('starts'), False),
                         date_ends = parse_date(a.get('ends'), False),
                         user = request.user,
                         poi = poi,
                         done = True if parse_date(a.get('done_when'), False) else False,
                         done_when = parse_date(a.get('done_when'), False),
                         active = True if a.get('active', True) else False,
                         )
            if a.get('client_id', None) is not None:  # la alerta no estaba sincronizada
                temp_alert[int(alert.id)] = a.get('client_id')
                           
        response = []
        alerts = Alert.objects.get_by_last_sync(request.user, last_sync)
        for a in alerts:
            if int(a.id) in temp_alert:  # añadir alerta no sincro
                dict = a.to_dict()
                dict['client_id'] = temp_alert[int(a.id)]
                response.append(dict)
            else:
                response.append(a.to_dict())
        alertsDel =  _Deleted_Alert.objects.get_by_last_sync(request.user, last_sync)
        for a in alertsDel:
            sync_deleted.append({'id': a.id})
        from time import mktime
        from datetime import datetime
        return [int(mktime(datetime.now().timetuple())), response, sync_deleted]
    except DeadlineExceededError:
        return DeadlineException


@jsonrpc_method('report_bug', authenticated=False)
def report_bug(request, bugs):
    from models import _Report_Bug
    from google.appengine.ext import db
    try:
        for b in bugs:
            datetime = parse_date(b.get('datetime'))
            from geouser.models import User
            u = User.objects.get_by_email(b.get('email'))
            report = _Report_Bug(user=u, msg=b.get('msg'), datetime=datetime)
            db.put_async([report])
    except:
        raise
        return False
    return True


@jsonrpc_method('view_timeline', authenticated=need_authenticate)
def view_timeline(request, username, query_id=None):
    if username == request.user.username:
        timelines = request.user.get_activity_timeline(query_id=query_id)
        return timelines
    else:
        from geouser.models import User
        user = User.objects.get_by_username(username)
        if user is not None:
            timelines = user.get_profile_timeline(query_id=query_id)
            return timelines
    raise InvalidRequestError


@jsonrpc_method('sync_alertlist', authenticated=need_authenticate)
def sync_alertlist(request, last_sync, modified=[], deleted=[]):
    """
        Sincroniza las listas de alertas
        
        :param last_sync: Ultima fecha de sincronizacion, en epoch
        :type last_sync: :class:`integer`
        :param modified: lista con las listas de alertas modificadas (en diccionario)
        :param deleted: lista con las listas de alertas a borrar (sus ids)
    """
    from geolist.models import ListAlert, List, _Deleted_List # FIXME: crear _Deleted_List
    from geoalert.models import Alert
    
    if type(modified) != type(list()) or type(deleted) != type(list()):
        raise InvalidParamsError
    sync_deleted = []
    temp_list = {}
    last_sync = parse_date(last_sync)
    parse_listdeleted(deleted, request.user)
    for l in modified:
        id = l.get('id', None)
        if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
            old = List.objects.get_by_id_user(id, request.user)
            if not old:  # no existe en la BD, fue borrada.
                sync_deleted.append({'id': id})
                continue
            if parse_date(l.get('modified')) <= old.modified:
                continue
        keys_to_add = []
        for i in l.get('instances'):
            keys_to_add.append(i)
        keys_to_del = []
        for i in l.get('delete_instances'):
            keys_to_del.append(i)
        new_list = ListAlert.insert_list(request.user, id=id,
                                          name=l.get('name'),
                                          instances=keys_to_add)
        new_list.update(instances_del=keys_to_del)
        if l.get('client_id', None) is not None:  # la alerta no estaba sincronizada
            temp_list[int(new_list.id)] = l.get('client_id')
    response = []
    lists = ListAlert.objects.get_by_last_sync(request.user, last_sync)
    for alist in lists:
        if int(alist.id) in temp_list:  # añadir alerta no sincro
            dict = alist.to_dict()
            dict['client_id'] = temp_list[int(alist.id)]
            response.append(dict)
        else:
            response.append(alist.to_dict())
    listsDel =  _Deleted_List.objects.get_by_last_sync(request.user, last_sync, ListAlert.kind())
    for l in listsDel:
        sync_deleted.append({'id': l.id})
    from time import mktime
    from datetime import datetime
    return [int(mktime(datetime.now().timetuple())), response, sync_deleted]
