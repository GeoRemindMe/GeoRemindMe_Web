# coding=utf-8

from signals import comment_new, vote_new, vote_deleted
from geouser.models_acc import UserTimeline, UserTimelineSystem

def new_comment(sender, **kwargs):
    from google.appengine.ext.deferred import defer
    from geoalert.models import Suggestion
    sender.instance.put(from_comment=True)
    timeline = UserTimelineSystem(user = sender.user, instance = sender, msg_id=120)
    from google.appengine.ext import db
    p = db.put_async([timeline])
    if hasattr(sender.instance, '_vis'):
        timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=120, _vis=sender.instance._get_visibility())
        timelinePublic.put()
    if isinstance(sender.instance, Suggestion):
        defer(sender.user.settings.notify_suggestion_comment, sender.key())
        sender.instance.counters.set_comments()
    p.get_result()
comment_new.connect(new_comment)

def new_vote(sender, **kwargs):
    from geoalert.models import Suggestion
    from geovote.models import Comment
    if isinstance(sender.instance, Suggestion):
        influenced = sender.instance.user.counters_async()
        supported = sender.user.counters_async()
        timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=305, _vis=sender.instance._get_visibility())
        timelinePublic.put()
        i = influenced.next()
        s = supported.next()
        i.set_influenced()
        s.set_supported()
    elif isinstance(sender.instance, Comment):
        timelinePublic = UserTimeline(user = sender.user, instance = sender, msg_id=125, _vis=sender.instance._get_visibility())
        timelinePublic.put()
vote_new.connect(new_vote)


def deleted_vote(sender, **kwargs):
    from geoalert.models import Suggestion
    if isinstance(sender.instance, Suggestion):
        influenced = sender.instance.user.counters_async()
        sender.user.counters.set_supported(-1)
        i = influenced.next()
        i.set_influenced(-1)
vote_deleted.connect(deleted_vote)