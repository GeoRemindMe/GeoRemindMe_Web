# coding=utf-8

from signals import comment_new, comment_deleted, vote_new, vote_deleted
from geoalert.signals import suggestion_deleted
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

def deleted_comment(sender, **kwargs):
    from geovote.models import Vote
    timeline = UserTimeline.objects.get_by_instance_user(sender, sender.user)
    votes = Vote.all().filter('instance =', sender).run()
    for t in timeline:
        t.delete()
    for vote in votes:
        vote.delete()
comment_deleted.connect(deleted_comment)
    
def deleted_vote(sender, **kwargs):
    from geoalert.models import Suggestion
    from geouser.models_acc import UserTimelineBase
    if isinstance(sender.instance, Suggestion):
        influenced = sender.instance.user.counters_async()
        sender.user.counters.set_supported(-1)
        i = influenced.next()
        i.set_influenced(-1)
    timelines = UserTimelineBase.all().filter('instance =', sender).run()
    for timeline in timelines:
        timeline.delete()
        
vote_deleted.connect(deleted_vote)

def deleted_suggestion(sender, **kwargs):
    from geouser.models_acc import UserTimelineBase
    from geovote.models import Comment, Vote
    comments = Comment.all().filter('instance =', sender).run()
    votes = Vote.all().filter('instance =', sender).run()
    for comment in comments:
        comment.delete()
    for vote in votes:
        vote.delete()
suggestion_deleted.connect(deleted_suggestion)