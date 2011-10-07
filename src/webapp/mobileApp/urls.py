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


urlpatterns = patterns('mobileApp.views',
    url(r'^$', 'login_panel', {}, 'mob_login_panel'),
    url(r'^dashboard/$', 'dashboard', {}, 'mob_dashboard'),
    url(r'^notifications/$', 'notifications', {}, 'mob_notifications'),
    url(r'^settings/$', 'profile_settings', {}, 'mob_profile_settings'),
    url(r'^settings/edit/$', 'edit_settings', {}, 'mob_edit_settings'),
    url(r'^user/edit/$', 'edit_profile', {}, 'mob_edit_profile'),
    url(r'^user/(?P<username>[^/]*)/$', 'profile', {}, 'mob_public_profile'),
    url(r'^user/(?P<username>[^/]*)/followers/$', 'followers_panel', {}, 'mob_followers_panel'),
    url(r'^user/(?P<username>[^/]*)/followings/$', 'followings_panel', {}, 'mob_followings_panel'),
    url(r'^suggestions/$', 'user_suggestions', {}, 'mob_user_suggestions'),
    url(r'^suggestions/edit/(?P<suggestion_id>\d+)/$', 'edit_suggestion', {}, 'mob_edit_suggestions'),
    url(r'^suggestions/add/$', 'add_suggestion',{},'mob_add_suggestion'),
    url(r'^suggestion/(?P<slug>[^/]*)/$', 'view_suggestion',{},'mob_view_suggestion'),
    url(r'^list/(?P<id>[^/]*)/$', 'view_list',{},'mob_view_list'),
    url(r'^place/(?P<place_id>[^/]*)/$', 'view_place',{},'mob_view_place'),
    url(r'^tag/(?P<slug>[^/]*)/suggestions/$', 'view_tag_suggestions',{},'mob_view_tag_suggestions'),
    url(r'^search/$', 'search_suggestions',{}),
    url(r'^search/(?P<term>[^/]*)/$', 'search_suggestions',{},'mob_search_suggestions'),
)
