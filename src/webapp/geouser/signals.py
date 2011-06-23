# coding=utf-8

import django.dispatch

# se registra un nuevo usuario
user_new = django.dispatch.Signal(providing_args=['status'])

# se da de alta el acceso desde una red social
user_social_new = django.dispatch.Signal()

# tiene un nuevo follower
user_follower_new = django.dispatch.Signal(providing_args=['following'])

# deja de seguir a otro usuario
user_following_deleted = django.dispatch.Signal(providing_args=['following'])

# hay que añadir al timeline publico
user_timeline_new = django.dispatch.Signal(providing_args=['user', 'msg', 'instance', 'vis'])