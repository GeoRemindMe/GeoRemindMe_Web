# coding=utf-8

import django.dispatch
from georemindme.signals import invitation_changed


list_new = django.dispatch.Signal()
list_deleted = django.dispatch.Signal()
list_modified = django.dispatch.Signal()
list_following_new = django.dispatch.Signal(providing_args=['user'])
list_following_deleted = django.dispatch.Signal(providing_args=['user'])
