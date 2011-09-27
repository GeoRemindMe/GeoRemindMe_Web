# coding=utf-8

import logging
from django.conf import settings
from signals import *
from exceptions import *

from geouser.models_acc import UserTimelineSystem, UserTimeline
from models_poi import *



def new_alert(sender, **kwargs):
    '''
    Se registra una nueva alerta
    '''
    from models import Alert, AlertSuggestion
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=200)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=320, visible=False)
    else:
        return
    timeline.put()
    sender.user.counters.set_alerts(value=+1)
alert_new.connect(new_alert)


def modified_alert(sender, **kwargs):
    '''
    Se modifica una alerta
    '''
    from models import Alert, AlertSuggestion
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=201)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=321, visible=False)
    else:
        return
    timeline.put()
alert_modified.connect(modified_alert)


def deleted_alert(sender, **kwargs):
    '''
    Se borra una alerta
    '''
    from models import Alert, AlertSuggestion
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=202)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=322, visible=False)
    else:
        return
    timeline.put()
    sender.user.counters.set_alerts(value=-1)
alert_deleted.connect(deleted_alert)


def done_alert(sender, **kwargs):
    from models import Alert, AlertSuggestion
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=203)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=323, visible=False)
    else:
        return
    timeline.put()
alert_done.connect(done_alert)


def new_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=300)
    timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=300, _vis=sender._get_visibility())
    p = db.put_async([timeline])
    sender.user.counters.set_suggested()
    if sender._is_public():
        from google.appengine.ext.deferred import defer, PermanentTaskFailure 
        try:
            defer(sender.insert_ft)
        except PermanentTaskFailure, e:
            from georemindme.models_utils import _Do_later_ft
            later = _Do_later_ft(instance_key=sender.key())
            later.put()
            import logging
            logging.error('ERROR FUSIONTABLES %s: %s' % (sender.id, e))
    timelinePublic.put()
    p.get_result()
suggestion_new.connect(new_suggestion)


def modified_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=301)
    timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=301, _vis=sender._get_visibility())
    db.put([timeline, timelinePublic])
#suggestion_modified.connect(modified_suggestion)


def deleted_suggestion(sender, **kwargs):
    from geouser.models_acc import UserTimelineBase
    query = UserTimelineBase.all().filter('instance =', sender.key()).run()
    kwargs['user'].counters.set_suggested(-1)
    for q in query:
        q.delete()
suggestion_deleted.connect(deleted_suggestion)


def new_following_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=303, visible=False)
    p = timeline.put_async()
    sender.counters.set_followers(+1)
    p.get_result()
    from google.appengine.ext.deferred import defer
    defer(sender.user.settings.notify_suggestion_follower, sender.key(), kwargs['user'].key())
    if sender.user is not None:
        if kwargs['user'].key() != sender.user.key():
            from geouser.models_utils import _Notification
            notification = _Notification(owner=sender.user, timeline=timeline)
            notification.put()
suggestion_following_new.connect(new_following_suggestion)


def deleted_following_suggestion(sender, **kwargs):
    from models import AlertSuggestion
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=304, visible=False)
    p = timeline.put_async()
    alertsuggestion = AlertSuggestion.objects.get_by_sugid_user(sender.id, kwargs['user'])
    if alertsuggestion is not None:
        alertsuggestion.delete()
    sender.counters.set_followers(-1)
    p.get_result()
suggestion_following_deleted.connect(deleted_following_suggestion)


def new_privateplace(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=400)
    timeline.put()
#privateplace_new.connect(new_privateplace)


def modified_privateplace(sender, **kwargs):    
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=401)
    timeline.put()
#privateplace_modified.connect(modified_privateplace)


def deleted_privateplace(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=402)
    timeline.put()
#privateplace_deleted.connect(deleted_privateplace)


def new_place(sender, **kwargs):
    #timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=450)
    #timeline.put()
    from google.appengine.ext.deferred import defer, PermanentTaskFailure 
    try:
        defer(sender.insert_ft)
    except PermanentTaskFailure, e:
        from georemindme.models_utils import _Do_later_ft
        later = _Do_later_ft(instance_key=sender.key())
        later.put()
        import logging
        logging.error('ERROR FUSIONTABLES %s: %s' % (sender.id, e))
place_new.connect(new_place)


def modified_place(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=451)
    timeline.put()
#place_modified.connect(modified_place)


def deleted_place(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=452)
    timeline.put()
#place_deleted.connect(deleted_place)
