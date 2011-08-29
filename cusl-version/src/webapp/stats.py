from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.hashcompat import sha_constructor
from google.appengine.ext import db
from google.appengine.api import users
from georemindme.models import User, GoogleUser, GeoUser, Alert

class Stats_base(db.Model):
    date = db.DateTimeProperty(required=True)
    new = db.IntegerProperty(default=0, required=True)
    total = db.IntegerProperty(default=0, required=True)
    
class Stats_user(Stats_base):
    pass

class Stats_geouser(Stats_user):
    pass

class Stats_googleuser(Stats_user):
    pass

class Stats_alert_new(Stats_base):
    pass

class Stats_alert_done(Stats_base):
    pass
    
def stats_daily(request):
    if request.META.get('HTTP_X_APPENGINE_CRON', 'false') == 'true':
        _get_stats(model=GeoUser, model_stats=Stats_geouser)
        _get_stats(model=GoogleUser, model_stats=Stats_googleuser)
        _get_stats(model=User, model_stats=Stats_user)
        _get_stats(model=Alert, model_stats=Stats_alert_new)
        _get_stats(model=Alert, model_stats=Stats_alert_done, order_field='done_when')
        
    return HttpResponse()
        
        
def _get_stats(model=User, model_stats=Stats_user, order_field='created'):
    newdate = datetime.now()
    lastStat = model_stats.all().order('-date').get()
    if not lastStat:
        u = model.all().order(order_field).get()
        if not u:
            return
        lastStat = model_stats(date=u.created, new=0, total=0)
        
    new = model.all(keys_only=True).filter('%s >=' % order_field, lastStat.date).count()
    if new == 1000:
        i = 1
        while new == 1000*i:
            new += model.all(keys_only=True).filter('%s >=' % order_field, lastStat.date).fetch(offset=1000*i, limit=1000).count()
            i += 1
    newStat = model_stats(date=newdate, new=new, total=lastStat.total+new)
    newStat.put()
    
    return