# coding=utf-8

"""
.. module:: Cron
    :platform: appengine
    :synopsis: Funciones cron
"""


from django.http import HttpResponse, HttpResponseForbidden
from google.appengine.ext import db
from libs.decorator import decorator


@decorator
def cron_required(func, *args, **kwargs):
    from google.appengine.api import users
    request = args[0]
    if request is None:
        return func(*args, **kwargs)
    if 'HTTP_X_APPENGINE_CRON' in request.META:
        return func(*args, **kwargs)
    user = request.session.get('user')
    if (user and user.is_admin()) or users.is_current_user_admin():
        return func(*args, **kwargs)
    return HttpResponseForbidden("Cron only")


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
    

#@cron_required
#def stats_daily(request):
#    from geoalert.models import  *
#    _get_stats(model=User, model_stats=Stats_user)
#    _get_stats(model=Alert, model_stats=Stats_alert_new)
#    _get_stats(model=Alert, model_stats=Stats_alert_done, order_field='done_when')
#    return HttpResponse()
#   
#        
#        
#def _get_stats(model=User, model_stats=Stats_user, order_field='created'):
#    newdate = datetime.now()
#    lastStat = model_stats.all().order('-date').get()
#    if not lastStat:
#        u = model.all().order(order_field).get()
#        if not u:
#            return
#        lastStat = model_stats(date=u.created, new=0, total=0)
#        
#    new = model.all(keys_only=True).filter('%s >=' % order_field, lastStat.date).count()
#    if new == 1000:
#        i = 1
#        while new == 1000*i:
#            new += model.all(keys_only=True).filter('%s >=' % order_field, lastStat.date).fetch(offset=1000*i, limit=1000).count()
#            i += 1
#    newStat = model_stats(date=newdate, new=new, total=lastStat.total+new)
#    newStat.put()
#    
#    return


@cron_required
def clean_sessions(request):
    from geomiddleware.sessions.models import _Session_Data
    from datetime import datetime
    import logging
    logging.info('limpiando sesiones...')
    sessions = _Session_Data.all().filter('expires <', datetime.now()).run()
    try:
        db.delete([session for session in sessions])
    except:
        raise
        pass
    return HttpResponse()


@cron_required
def report_notify(request, time):
    # correos de los usuarios
    from geouser.models_acc import UserSettings
    from geouser.models_utils import _Report_Account_follower, _Report_Suggestion_changed
    users_settings = UserSettings().all().filter('time_notification_account =', time).run()
    for user in users_settings:
        user = user.parent()
        report = _Report_Account_follower.get_by_key_name('report_account_follower_%d' % user.id)
        if report is not None:
            report.send_notification(user)
            report.delete()
    # correos de resumen de sugerencia
    from geouser.mails import send_notification_suggestion_summary
    users = UserSettings().all().filter('time_notification_suggestion_follower =', time).run()
    for user in users:
        user = user.parent()
        reports = _Report_Suggestion_changed.all().filter('user =', user).run()
        _Report_Suggestion_changed.send_notification(reports, user)
    # TODO: correos de comentarios
    return HttpResponse()
