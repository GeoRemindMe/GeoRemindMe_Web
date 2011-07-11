"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the Affero General Public License (AGPL) as published 
by Affero, as published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

You should have received a copy of the GNU Affero General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('facebookApp.views',
    url(r'^$', 'login_panel', {}, 'fb_login_panel'),
    url(r'^dashboard/$', 'dashboard', {}, 'fb_dashboard'),
    url(r'^settings/$', 'profile_settings', {}, 'fb_profile_settings'),
    url(r'^settings/edit/$', 'edit_settings', {}, 'fb_edit_settings'),
    url(r'^user/edit/$', 'edit_profile', {}, 'fb_edit_profile'),
    url(r'^user/(?P<username>[^/]*)/$', 'profile', {}, 'fb_public_profile'),
    url(r'^user/(?P<username>[^/]*)/followers/$', 'followers_panel', {}, 'fb_followers_panel'),
    url(r'^user/(?P<username>[^/]*)/followings/$', 'followings_panel', {}, 'fb_followings_panel'),
    url(r'^suggestions/$', 'user_suggestions', {}, 'fb_user_suggestions'),
    url(r'^suggestions/add/$', 'add_suggestion',{},'fb_add_suggestion'),
    url(r'^test_user/$', 'test_users', {}, 'fb_test_user'),
    url(r'^get_test_user/$', 'get_test_users', {}, 'fb_get_test_user'),
)
