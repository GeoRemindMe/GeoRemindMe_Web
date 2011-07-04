# coding=utf-8

from signals import *

def new_comment_event(sender, **kwargs):
    from geouser.models_acc import UserSettings
    from google.appengine.ext.deferred import defer
    defer(sender.user.settings.notify_suggestion_comment, sender.key())
comment_event_new.connect(new_comment_event)

from models import *