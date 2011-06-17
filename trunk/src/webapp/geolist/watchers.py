# coding=utf-8

import logging

from signals import *
from exceptions import *

from geouser.models_acc import UserTimelineSystem


def new_list(sender, **kwargs):
    if isinstance(sender, ListAlert):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=250, instance=sender)
    elif isinstance(sender, ListUser):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=150, instance=sender)
    elif isinstance(sender, ListSuggestion):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=350, instance=sender)
    else:
        return
    timeline.put()
list_new.connect(new_list)

def modified_list(sender, **kwargs):
    if isinstance(sender, ListAlert):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=251, instance=sender)
    elif isinstance(sender, ListUser):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=151, instance=sender)
    elif isinstance(sender, ListSuggestion):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=351, instance=sender)
        from georemindme.tasks import NotificationHandler
        NotificationHandler().list_followers_notify(sender)
    else:
        return
    timeline.put()
list_modified.connect(modified_list)

def deleted_list(sender, **kwargs):
    if isinstance(sender, ListAlert):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=252, instance=sender)
    elif isinstance(sender, ListUser):
        timeline = UserTimelineSystem(user=sender.user.key(), msg_id=152, instance=sender)
    elif isinstance(sender, ListSuggestion):
        timeline = UserTimelineSystem(user=self.user, msg_id=352, instance=self)
    else:
        return
    timeline.put()
list_deleted.connect(deleted_list)

def new_following_list(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=353)
    timeline.put()
list_following_new.connect(new_following_list)

def deleted_following_list(sender, **kwargs):
    timeline = UserTimelineSystem(user = kwargs['user'], instance = sender, msg_id=354)
    timeline.put()
list_following_deleted.connect(deleted_following_list)

from models import *