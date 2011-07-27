# coding=utf-8

import django.dispatch


comment_new = django.dispatch.Signal()
comment_deleted = django.dispatch.Signal()

vote_new = django.dispatch.Signal()
vote_deleted = django.dispatch.Signal()