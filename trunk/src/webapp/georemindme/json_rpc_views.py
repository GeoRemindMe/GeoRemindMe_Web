from datetime import datetime,timedelta

from django.utils import simplejson
from django.conf import settings

from georemindme.models import User,GeoUser, POI, Point, Business, Alert

from rpc_server.models import UserRPC
from rpc_server.decorators import jsonrpc_function, jsonrpc_logged_function
from rpc_server.exceptions import GeoException



@jsonrpc_function
def login(email, password):
	"""
		Log a user and creates a new UserRPC session ID
		The user_id should be send with all the request.
	"""
	u = User.objects.get_by_email(email=email)
	if u is not None:
		if u.check_password(password):
			
			if not u.is_confirmed() and u.created+timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS) < datetime.now():
				u.send_confirm_code()
				raise Exception( GeoException.NO_CONFIRMED )
				
			urpc = UserRPC.objects.get_by_email(email=u.email)
			if urpc is None:
				urpc = UserRPC(email=email,realuser = u)
			urpc.put()			
			return urpc.session_id
	raise Exception( GeoException.BAD_EMAIL_PASSWORD )

@jsonrpc_function
def register(email, password):
	"""
		Register a user
		returns True if sucessful
	"""
	try:
		u = GeoUser(email=email, password=password)
		u.send_confirm_code()
		u.put()
		if u is not None:
			return True	
	except:
		pass
	raise Exception( GeoException.BAD_EMAIL_PASSWORD )

@jsonrpc_function
def sync(session_id, last_sync, modified):
	"""
		Sync with devices
	"""	
	
	def parse_date(date,excep=True):
		
		if date is None:
			if excep:
				raise Exception( GeoException.INVALID_REQUEST )
			else:
				return None
		
		if type(date) in (str,unicode,) and not date.isdigit():
			if excep:
				raise Exception( GeoException.INVALID_REQUEST )
			else:
				return None

		return datetime.fromtimestamp(date)
	
	u = UserRPC.objects.get_by_id(session_id)
	if u is None or not u.is_valid():
		raise Exception( GeoException.INVALID_SESSION )

	last_sync = parse_date(last_sync)

	# 1) parse last_sync and modified to datetime
	#last_sync = datetime.datetime.fromtimestamp(last_sync)
	
	# modified is sent as string
	if modified:
		try:
			modified = simplejson.loads(modified)
		except ValueError:
			raise Exception( GeoException.INVALID_REQUEST )
	else:
		modified = []
	
	for a in modified:

		# comented for the beta
		""""
		if a.get('point'):
			poi = Point( **(a['point']) )
			del a['point']
		elif a.get('business'):
			poi = Business( **(a['business']) )
			del a['business']
		else:
			raise Exception( GeoException.INVALID_REQUEST )"""

		# check if the input data is ok
		if not isinstance(a.get('points'),list) or not len(a.get('points')) or not isinstance(a.get('points')[0],list) or not len(a.get('points')[0]) == 2:
			raise Exception( GeoException.INVALID_REQUEST )	

		if not a.get('id'): # the alert is new
			pass
			# not implemented
			
			# 1) create the poi (point)
			# 2) create the alert
			# 3) save and append to return
			
		else:
			
			if not isinstance(a.get('id'),int):
				raise Exception( GeoException.INVALID_REQUEST )
			
			old = Alert.objects.get_by_id_user(a.get('id'), u.realuser)
			
			if not old:
				raise Exception( GeoException.INVALID_REQUEST )
			
			# sync control
			if parse_date(a.get('modified')) <= old.modified:
				continue
			
			# poi data, only point considered
			from google.appengine.ext.db import GeoPt
			poi = old.poi
			# poi data
			poi.created = parse_date(a.get('created'))
			poi.modified = parse_date(a.get('modified'))
			poi.name = a.get('name',u'')
			# point data
			poi.address = u''
			poi.business = u''
			poi.point = GeoPt(a['points'][0][0],a['points'][0][1])
			poi.put()
			
			done_when = parse_date(a.get('done_when'),False)
			
			old.name = a.get('name',u'')
			old.starts = parse_date(a.get('starts'),False)
			old.ends = parse_date(a.get('ends'),False)
			old.description = a.get('description',u'')
			old.created = parse_date(a.get('created'))
			old.modified = parse_date(a.get('modified'))
			old.done_when = done_when
			if old.is_done() and not done_when or not old.is_done() and done_when:
				old.toggle_done()
			if not a.get('active') is None and old.is_active() != a.get("active"):
				old.toggle_active() 
			old.set_distance(0)
			old.put()

	def compare(a, b):
		return cmp(a.modified, b.modified) # compare as integers

	# return the alerts modified after last sync
	alerts = Alert.objects.get_by_last_sync(u.realuser, last_sync )
	alerts.sort(compare)
	ret = []
	
	import time
	
	for a in alerts:
		ret.append(dict(
					id=a.id,
					points=[ (a.poi.point.lat,a.poi.point.lon) ],
					name = a.name,
					starts = int(time.mktime(a.starts.timetuple())) if a.starts else 0,
					ends = int(time.mktime(a.ends.timetuple())) if a.ends else 0,
					created = int(time.mktime(a.created.timetuple())) if a.created else 0,
					modified = int(time.mktime(a.modified.timetuple())) if a.modified else 0,
					done_when = int(time.mktime(a.done_when.timetuple())) if a.done_when else 0,
					done = a.is_done(),
					active = a.is_active(),
					description = a.description
					)
				)
				
	return (int(time.mktime(datetime.now().timetuple())), ret)



@jsonrpc_function
def getProximityAlerts(session_id, lat, long):
	"""
		Get the Alerts near to the user position
	"""
	
	u = UserRPC.objects.get_by_id(session_id)
	if u is None or not u.is_valid():
		raise Exception( GeoException.INVALID_SESSION )
		
	from geobox import proximity_alerts

	alerts = proximity_alerts(u.realuser, lat, long)
	##return simplejson.dumps( [ a.__dict__ for a in alerts ] )
	
	# now only works for Point alerts (no Business alerts)
	ret = [
		dict(id=str(alert.key()), # alert's key
		points=[ (alert.poi.point.lat,alert.poi.point.lon) ] # point of the alert
		
		) for alert in alerts]
	
	return ret
	
	


