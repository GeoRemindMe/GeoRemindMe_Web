# coding=utf-8

from signals import *

def new_comment(sender, **kwargs):
    from geouser.models_acc import UserSettings
    from google.appengine.ext.deferred import defer
    from geoalert.models import Event
    if isinstance(sender.instance, Event):
        defer(sender.user.settings.notify_suggestion_comment, sender.key())
comment_new.connect(new_comment)