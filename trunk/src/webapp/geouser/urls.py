# coding=utf-8
from django.conf.urls.defaults import *


urlpatterns = patterns('geouser.views',
    (r'^login/$', 'login'),
    (r'^login/google/$', 'login_google'),
    (r'^login/twitter/$', 'login_twitter'),
    (r'^login/facebook/$', 'login_facebook'),
    (r'^dashboard/$', 'dashboard'),
    (r'^user/(?P<username>[^/]*)/$', 'public_profile'),
    (r'^logout/$', 'logout'),
)