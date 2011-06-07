# coding=utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('geoalert.views',
    (r'^event/(?P<id>[^/]*)/$', 'suggestion_profile'),
    
)