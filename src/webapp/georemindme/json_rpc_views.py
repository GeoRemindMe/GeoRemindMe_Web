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

@jsonrpc_method('login', authenticated=False)
def login(request, email, password):
    '''
        Log a user and creates a new UserRPC session ID.
        The user_id should be send with all the request.
    '''
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
    

@jsonrpc_method('register', validate=False, authenticated=False)
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

@jsonrpc_method('sync', validate=False, authenticated=False)
def sync(request, session_id, last_sync, modified=[]):
    '''
        Sync with devices
    '''
    if not isinstance(session_id, basestring):
        raise InvalidParamsError
    if type(modified) != type(list()):
        raise InvalidParamsError
    last_sync= float(last_sync)
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
    # cuando se envie la sesion id por cabeceras HTTP esta parte no es necesaria
    # user estaria en request.user
    session = SessionStore.load(session_id=session_id, from_cookie=False, from_rpc=True)
    try:
        u = session['user']
        if u is None:
            raise
    except:
        raise BadSessionException
    session.put()
    
    last_sync = parse_date(last_sync)
    response = []
    deleted = []
    for a in modified:
        if type(a) != type(dict()):
            raise InvalidParamsError
        id = a.get('id', None)
        if id is not None:
            if not isinstance(id, int):  # invalid type
                raise InvalidParamsError
            old = Alert.objects.get_by_id_user(id, u)
            # sync control
            if parse_date(a.get('modified')) <= old.modified:
                continue
            if not old:  # unknow alert
                deleted = id
                continue
        poi = PrivatePlace.get_or_insert(name = '',
                                         location = GeoPt(a.get('x'), a.get('y')),
                                         address = '',
                                         user = u)
        alert = Alert.update_or_insert(
                     id = id,
                     name = a.get('name', u''),
                     description = a.get('description', u''),
                     date_starts = parse_date(a.get('starts'), False),
                     date_ends = parse_date(a.get('ends'), False),
                     user = u,
                     poi = poi,
                     done = True if parse_date(a.get('done_when'), False) else False,
                     done_when = parse_date(a.get('done_when'), False),
                     active = True if a.get('active', False) else False,
                     )            
# return the alerts modified after last sync
    alerts = Alert.objects.get_by_last_sync(u, last_sync)
    for a in alerts:
        response.append(a.to_dict())
    return [int(time.mktime(datetime.now().timetuple())), response, deleted]



@jsonrpc_method('getProximityAlerts', validate=False)
def getProximityAlerts(request, session_id, lat, long):
    '''
        Get the Alerts near to the user position
    '''
    session = SessionStore.load(session_id, from_cookie=False, from_rpc=True)
    session.put()
    u = session['user'] 
    from geoalert.geobox import proximity_alerts

    alerts = proximity_alerts(u, lat, long)
    ##return simplejson.dumps( [ a.__dict__ for a in alerts ] )
    
    # now only works for Point alerts (no Business alerts)
    ret = [
        dict(id=str(alert.key()), # alert's key
        points=[ (alert.poi.point.lat, alert.poi.point.lon) ] # point of the alert
        
        ) for alert in alerts]
    
    return ret
