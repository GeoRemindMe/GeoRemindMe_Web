# coding=utf-8

from django.dispatch import Signal

timeline_added = Signal(providing_args=["timeline",])

follower_added = Signal(providing_args=["follower, followee"])
follower_deleted = Signal(providing_args=["follower, followee"])