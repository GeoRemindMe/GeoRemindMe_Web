# coding=utf-8

from datetime import datetime, timedelta
import time

from django.utils import simplejson

from google.appengine.ext.db import GeoPt

from geoalert.models import *
from geoalert.models_poi import *
from geouser.models import User
from geouser.funcs import login_func
from geomiddleware.sessions.store import SessionStore

from libs.jsonrpc import jsonrpc_method
from libs.jsonrpc.exceptions import *

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
    

@jsonrpc_method('register', authenticated=False)
def register(request, email, password):
    '''
        Register a user
        returns True if sucessful
    '''
    email = unicode(email)
    password = unicode(password)
    try:
        u = User.register(email=email, password=password)
        if u is not None:
            return True    
    except:
        pass
    raise RegisterException

@jsonrpc_method('sync_alert', authenticated=need_authenticate)
def sync_alert(request, last_sync, modified=[], deleted=[]):
    if type(modified) != type(list()) or type(deleted) != type(list()):
        raise InvalidParamsError
    
    temp_alert = {}
    last_sync = parse_date(last_sync)
    for a in modified:

        id = a.get('id', None)
        if id is not None:  # la alerta ya estaba sincronizada, la actualizamos
            old = Alert.objects.get_by_id_user(id, request.user)
            # sync control
            if parse_date(a.get('modified')) <= old.modified:
                continue
            if not old:  # unknow alert
                deleted_to_sync.append(id)
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
                     active = True if a.get('active', False) else False,
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
    return [int(time.mktime(datetime.now().timetuple())), response, deleted]

@jsonrpc_method('report_bug', authenticated=False)
def report_bug(request, email, msg, datetime):
    from rpc_server.models import _Report_Bug
    try:
        datetime = parse_data(datetime)
        u = User.objects.get_by_email(email)
        bug = _Report_Bug(user=u, msg=msg, datetime=datetime)
        bug.put()
    except:
        return False
    return True
    