# coding=utf-8

import django.dispatch


comment_new = django.dispatch.Signal()

vote_suggestion_new = django.dispatch.Signal()
vote_comment_new = django.dispatch.Signal()
vote_list_new = django.dispatch.Signal()
