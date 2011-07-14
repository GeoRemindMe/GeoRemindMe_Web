# coding=utf-8
from django.conf.urls.defaults import *


urlpatterns = patterns('geouser.views',
    (r'^(?i)login/$', 'login'),
    (r'^(?i)login/google/$', 'login_google'),
    (r'^(?i)login/twitter/$', 'login_twitter'),
    (r'^(?i)login/facebook/$', 'login_facebook'),
    (r'^(?i)dashboard/$', 'dashboard'),
    (r'^(?i)user/(?P<username>[^/]*)/$', 'public_profile'),
    (r'^(?i)user/(?P<username>[^/]*)/picture/$', 'get_avatar', {}, 'user_avatar'),
    (r'^(?i)logout/$', 'logout'),
    (r'^(?i)confirm/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'confirm'),
    (r'^(?i)remind/$', 'remind_user'),
    (r'^(?i)remind/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'remind_user_code'),
    (r'^(?i)ext/google/perms/$', 'get_perms_google'),
    (r'^(?i)ext/google/contacts/$', 'get_contacts_google'),
    (r'^(?i)ext/twitter/perms/$', 'get_perms_twitter'),
    (r'^(?i)ext/twitter/contacts/$', 'get_friends_twitter'),
    url(r'^(?i)ext/close_window/$', 'close_window', {}, 'close_window'),
    (r'^update/$', 'update')
)