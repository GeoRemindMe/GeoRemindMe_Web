# coding=utf-8
from django.conf.urls.defaults import *

urlpatterns = patterns('geoalert.views',
    (r'^(?i)event/(?P<id>[^/]*)/$', 'suggestion_profile'),
    
)