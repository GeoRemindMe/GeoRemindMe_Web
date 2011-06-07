# coding=utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('geouser.views',
    (r'^event/(?P<id>[^/]*)/$', 'event_profile'),
    
)