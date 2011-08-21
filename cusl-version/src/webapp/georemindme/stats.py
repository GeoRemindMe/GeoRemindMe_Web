import os
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden
from google.appengine.ext import db
from geouser.models import User
from geoalert.models import  *

def admin_required(func):
    def _wrapper(*args, **kwargs):
        if 'HTTP_X_APPENGINE_CRON' in os.environ:
            return func(*args, **kwargs)
        session = args[0].session
        user = session.get('user')
        if user and user.is_admin():
            return func(*args, **kwargs)
        return HttpResponseForbidden()
    return _wrapper

class Stats_base(db.Model):
    date = db.DateTimeProperty(required=True)
    new = db.IntegerProperty(default=0, required=True)
    total = db.IntegerProperty(default=0, required=True)
    
class Stats_user(Stats_base):
    pass

class Stats_googleuser(Stats_user):
    pass

class Stats_alert_new(Stats_base):
    pass

class Stats_alert_done(Stats_base):
    pass
    

@admin_required
def stats_daily(request):
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