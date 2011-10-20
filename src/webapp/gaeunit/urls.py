# coding=utf-8

from django.conf.urls.defaults import *

urlpatterns = patterns('gaeunit.views',
    (r'^run/$', 'django_json_test_runner'),
    (r'^$', 'django_test_runner'),
)
