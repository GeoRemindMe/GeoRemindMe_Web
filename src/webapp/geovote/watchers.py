# coding=utf-8

from signals import comment_new, vote_new, vote_deleted

def new_comment(sender, **kwargs):
    from google.appengine.ext.deferred import defer
    from geoalert.models import Event
    sender.instance.put(from_comment=True)
    if isinstance(sender.instance, Event):
        defer(sender.user.settings.notify_suggestion_comment, sender.key())
comment_new.connect(new_comment)

def new_vote(sender, **kwargs):
    from geoalert.models import Suggestion
    if isinstance(sender.instance, Suggestion):
        influenced = sender.instance.user.counters_async()
        supported = sender.user.counters.set_supported()
        i = influenced.next()
        i.set_influenced()
vote_new.connect(new_vote)


def deleted_vote(sender, **kwargs):
    from geoalert.models import Suggestion
    if isinstance(sender.instance, Suggestion):
        influenced = sender.instance.user.counters_async()
        sender.user.counters.set_supported(-1)
        i = influenced.next()
        i.set_influenced(-1)
vote_deleted.connect(deleted_vote)