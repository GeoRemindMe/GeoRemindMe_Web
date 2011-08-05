# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geotags.views',
    (r'^(?i)tag/(?P<slug>[^/]*)/suggestions/$', 'view_tag_suggestions'),
)