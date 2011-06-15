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

from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import *

@jsonrpc_method('login', authenticated=False)
def login(request, email, password):
    '''
        Log a user and creates a new UserRPC session ID.
        The user_id should be send with all the request.
    '''
    email = str(email)
    password = str(password)
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
    email = str(email)
    password = str(password)
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
    session = SessionStore.load(session_id, from_cookie=False, from_rpc=True)
    u = session['user']
    session.put()
    last_sync = parse_date(last_sync)
    # modified is sent as string
    if modified:
        try:
            modified = simplejson.loads(modified)
        except ValueError:
            raise InvalidParamsError
    else:
        modified = []
    response = []
    deleted = []
    for a in modified:
        if not a.get('id'): # the alert is new
            poi = PrivatePlace.get_or_insert(name = '',
                                             location = GeoPt(a.get('x'), a.get('y')),
                                             address = '',
                                             user = u)
            alert = Alert.update_or_insert(
                         name = a.get('name', u''),
                         description = a.get('description', u''),
                         poi = poi,
                         date_starts = parse_date(a.get('starts'), False),
                         date_ends = parse_date(a.get('ends'), False),
                         user = u,
                         done = True if parse_date(a.get('done_when'), False) else False,
                         done_when = parse_date(a.get('done_when'), False),
                         active = True if a.get('active', False) else False,
                         )           
        else: # update an old alert
            if not isinstance(a.get('id'), int):  # invalid type
                raise InvalidParamsError
            old = Alert.objects.get_by_id_user(a.get('id'), u.realuser)
            if not old:  # unknow alert
                deleted = a.get('id')
                continue
            # sync control
            if parse_date(a.get('modified')) <= old.modified:
                continue
            poi = PrivatePlace.get_or_insert(name = '',
                                             location = GeoPt(a.get('x'), a.get('y')),
                                             address = '',
                                             user = u)
            old = Alert.update_or_insert(
                         id = a.get('id'), name = a.get('name', u''),
                         description = a.get('description', u''),
                         date_starts = parse_date(a.get('starts'), False),
                         date_ends = parse_date(a.get('ends'), False),
                         user = u,
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

    alerts = proximity_alerts(u.realuser, lat, long)
    ##return simplejson.dumps( [ a.__dict__ for a in alerts ] )
    
    # now only works for Point alerts (no Business alerts)
    ret = [
        dict(id=str(alert.key()), # alert's key
        points=[ (alert.poi.point.lat, alert.poi.point.lon) ] # point of the alert
        
        ) for alert in alerts]
    
    return ret
