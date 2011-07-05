# coding=utf-8

from datetime import datetime, timedelta
import time

from django.utils import simplejson

from google.appengine.ext.db import GeoPt

from geoalert.models import Alert, _Deleted_Alert
from geoalert.models_poi import *
from geolist.models import *
from geouser.models import User
from geouser.funcs import login_func

from libs.jsonrpc import jsonrpc_method
from libs.jsonrpc.exceptions import *
from libs.jsonrpc.views import *

def need_authenticate(username=None, password=None):
    raise BadSessionException
    
def parse_date(date, excep=True):
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
        return datetime.fromtimestamp(date)
    
def parse_alertdeleted(deleted, user):
    for a in deleted:  # borrar las alertas enviadas por el movil
        id = a.get('id', None)
        if id is not None:
            alert = Alert.objects.get_by_id_user(id, user)
            if alert is not None:
                alert.delete()

def parse_listdeleted(deleted, user):
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
    '''
        Register a user
        returns True if sucessful
    '''
    email = unicode(email)
    password = unicode(password)

    u = User.register(email=email, password=password)
    if u is not None:
        return True


@jsonrpc_method('sync_alert', authenticated=need_authenticate)
def sync_alert(request, last_sync, modified=[], deleted=[]):
    if type(modified) != type(list()) or type(deleted) != type(list()):
        raise InvalidParamsError
    sync_deleted = set()
    temp_alert = {}
    last_sync = parse_date(last_sync)
    parse_alertdeleted(deleted, request.user)
    for a in modified:
        id = a.get('id', None)
        if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
            old = Alert.objects.get_by_id_user(id, request.user)
            if not old:  # no existe en la BD, fue borrada.
                sync_deleted.add({'id': id})
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
        sync_deleted.add({'id': a.id})
    return [int(time.mktime(datetime.now().timetuple())), response, sync_deleted]


@jsonrpc_method('report_bug', authenticated=False)
def report_bug(request, bugs):
    from models import _Report_Bug
    try:
        for b in bugs:
            datetime = parse_date(b.get('datetime'))
            u = User.objects.get_by_email(b.get('email'))
            report = _Report_Bug(user=u, msg=b.get('msg'), datetime=datetime)
            db.put_async([report])
    except:
        raise
        return False
    return True


@jsonrpc_method('view_timeline', authenticated=need_authenticate)
def view_timeline(request, userid=None, query_id=None, page=1):
    if userid is None:
        timelines = request.user.get_timelineALL(page=page, query_id=query_id)
        return timelines
    

@jsonrpc_method('sync_alertlist', authenticated=need_authenticate)
def sync_alertlist(request, last_sync, modified=[], deleted=[]): 
    if type(modified) != type(list()) or type(deleted) != type(list()):
        raise InvalidParamsError
    sync_deleted = set()
    temp_list = {}
    last_sync = parse_date(last_sync)
    parse_listdeleted(deleted, request.user)
    for l in modified:
        id = l.get('id', None)
        if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
            old = List.objects.get_by_id_user(id, request.user)
            if not old:  # no existe en la BD, fue borrada.
                sync_deleted.add({'id': id})
                continue
            if parse_date(l.get('modified')) <= old.modified:
                continue
        keys_to_add = []
        for i in l.get('instances'):
            keys_to_add.add(Alert.get_by_id_user(id, request.user))
        keys_to_del = []
        for i in l.get('delete_instances'):
            keys_to_del.add(Alert.get_by_id_user(id, request.user))
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
        sync_deleted.add({'id': l.id})

    return [int(time.mktime(datetime.now().timetuple())), response, sync_deleted]
    

