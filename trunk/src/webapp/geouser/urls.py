# coding=utf-8
from django.conf.urls.defaults import *


urlpatterns = patterns('geouser.views',
    (r'^(?i)login/$', 'login'),
    (r'^(?i)login/google/$', 'login_google'),
    (r'^(?i)login/twitter/$', 'login_twitter'),
    (r'^(?i)login/facebook/$', 'login_facebook'),
    (r'^(?i)dashboard/$', 'dashboard'),
    (r'^(?i)user/(?P<username>[^/]*)/$', 'public_profile'),
    (r'^(?i)logout/$', 'logout'),
    (r'^(?i)confirm/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'confirm')
    (r'^(?i)remind/$', 'remind_user'),
    (r'^(?i)remind/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'remind_user_code')
)