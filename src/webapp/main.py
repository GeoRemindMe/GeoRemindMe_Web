#coding=utf-8

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

app = django.core.handlers.wsgi.WSGIHandler()
