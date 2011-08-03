# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geolist.views',
    (r'^(?i)list/(?P<id>[^/]\d+)/$', 'view_list'),
    
)