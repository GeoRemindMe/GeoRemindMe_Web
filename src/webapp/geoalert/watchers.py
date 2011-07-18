# coding=utf-8

import logging

from signals import *
from exceptions import *

from geouser.models_acc import UserTimelineSystem, UserTimeline
from models_poi import *


def new_alert(sender, **kwargs):
    '''
    Se registra una nueva alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=200)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=320)
    else:
        return
    timeline.put()
alert_new.connect(new_alert)

def modified_alert(sender, **kwargs):
    '''
    Se modifica una alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=201)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=321)
    else:
        return
    timeline.put()
alert_modified.connect(modified_alert)

def deleted_alert(sender, **kwargs):
    '''
    Se borra una alerta
    '''
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instancem = sender, msg_id=202)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=322)
    else:
        return
    timeline.put()
alert_deleted.connect(deleted_alert)

def done_alert(sender, **kwargs):
    if isinstance(sender, Alert):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=203)
    elif isinstance(sender, AlertSuggestion):
        timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=323)
    else:
        return
    timeline.put()
alert_done.connect(done_alert)

def new_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=300)
    timeline.put()
    if sender._is_public():
        timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=300)
        timelinePublic.put()
    sender.user.counters.set_suggested()
suggestion_new.connect(new_suggestion)

def modified_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=301)
    timeline.put()
    if sender._is_public():
        timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=301)
        timelinePublic.put()
    sender.user.counters.set_suggested(value=-1)
suggestion_modified.connect(modified_suggestion)

def deleted_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=302)
    timeline.put()
suggestion_deleted.connect(deleted_suggestion)

def new_following_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=333)
    timeline.put()
    from google.appengine.ext.deferred import defer
    defer(sender.user.settings.notify_suggestion_follower, sender.key(), kwargs['user'].key())
suggestion_following_new.connect(new_following_suggestion)

def deleted_following_suggestion(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=304)
    timeline.put()
suggestion_following_deleted.connect(deleted_following_suggestion)

def new_privateplace(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=400)
    timeline.put()
privateplace_new.connect(new_privateplace)

def modified_privateplace(sender, **kwargs):    
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=401)
    timeline.put()
privateplace_modified.connect(modified_privateplace)

def deleted_privateplace(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=402)
    timeline.put()
privateplace_deleted.connect(deleted_privateplace)

def new_place(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=450)
    timeline.put()
    sender.insert_ft()
place_new.connect(new_place)

def modified_place(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=451)
    timeline.put()
place_modified.connect(modified_place)

def deleted_place(sender, **kwargs):
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=452)
    timeline.put()
place_deleted.connect(deleted_place)


from models import *