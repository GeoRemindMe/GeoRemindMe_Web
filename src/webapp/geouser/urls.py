# coding=utf-8

"""
.. module:: urls
    :platform: appengine
    :synopsis: URLs de geouser
"""

from django.conf.urls.defaults import *


urlpatterns = patterns('geouser.views',
    (r'^(?i)login/$', 'login'),
    (r'^(?i)login/google/$', 'login_google'),
    (r'^(?i)login/twitter/$', 'login_twitter'),
    (r'^(?i)login/facebook/$', 'login_facebook'),
    (r'^(?i)dashboard/contacts$', 'dashboard_contacts', {}, 'dashboard_add_contacts'),
    (r'^(?i)dashboard/$', 'dashboard', {}, 'dashboard'),
    (r'^(?i)settings/$', 'profile_settings', {}, 'profile_settings'),
    (r'^(?i)settings/edit/$', 'edit_settings', {}, 'edit_settings'),
    (r'^(?i)user/edit/$', 'edit_profile', {}, 'edit_profile'),
    (r'^(?i)user/(?P<username>[^/]*)/picture/$', 'get_avatar', {}, 'user_avatar'),
    (r'^(?i)user/(?P<username>[^/]*)/$', 'public_profile',{},'public_profile'),
    (r'^(?i)logout/$', 'logout', {}, 'logout'),
    (r'^(?i)notifications/$', 'notifications', {}, 'notifications'),
    (r'^(?i)confirm/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'confirm'),
    (r'^(?i)remind/$', 'remind_user'),
    (r'^(?i)remind/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'remind_user_code'),
    (r'^(?i)ext/google/perms/$', 'get_perms_google'),
    (r'^(?i)ext/google/contacts/$', 'get_contacts_google'),
    #(r'^(?i)ext/twitter/perms/$', 'get_perms_twitter'),
    (r'^(?i)ext/twitter/contacts/$', 'get_friends_twitter'),
    url(r'^user/(?P<username>[^/]*)/followers/$', 'followers_panel', {}, 'followers_panel'),
    url(r'^user/(?P<username>[^/]*)/followings/$', 'followings_panel', {}, 'followings_panel'),
    url(r'^(?i)ext/close_window/$', 'close_window', {}, 'close_window'),
    (r'^update/$', 'update')
)
