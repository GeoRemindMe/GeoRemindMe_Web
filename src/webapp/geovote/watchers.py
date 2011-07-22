# coding=utf-8

from signals import comment_new

def new_comment(sender, **kwargs):
    from google.appengine.ext.deferred import defer
    from geoalert.models import Event
    sender.instance.put()
    if isinstance(sender.instance, Event):
        defer(sender.user.settings.notify_suggestion_comment, sender.key())
comment_new.connect(new_comment)