# coding=utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('geoalert.views',
    (r'^(?i)event/(?P<id>[^/]*)/$', 'suggestion_profile'),
    (r'^(?i)place/gref/(?P<reference>[^/]*)/$', 'add_from_google_reference'),
    (r'^(?i)place/(?P<slug>[^/]*)/$', 'view_place'),
)