# coding=utf-8

"""
.. module:: signals
    :platform: appengine
    :synopsis: Señales enviadas por Modelos comunes a todo el proyecto
"""


import django.dispatch

invitation_changed = django.dispatch.Signal()
