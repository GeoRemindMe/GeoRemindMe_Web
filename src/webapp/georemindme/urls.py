# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.


"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to




urlpatterns = patterns('georemindme.views',
    url(r'^$', 'login_panel'),
    url(r'^(?i)m/$', direct_to_template, {'template': 'mobile/index.html'}, 'georemindme.mobile'),
    url(r'^(?i)lang/$', 'set_language'),
    url(r'^(?i)general/$', direct_to_template, {'template': 'webapp/general.html'}),
    url(r'^(?i)clean/sessions/$', 'clean_sessions'),
    url(r'^(?i)tasks/email/$', 'email_worker'),
    url(r'^(?i)tasks/notify/timeline/$', 'timelinefollowers_worker'),
    url(r'^(?i)tasks/notify/list/$', 'list_notify_worker'),
    url(r'^(?i)reports/(?P<time>[^/]*)/$', 'report_notify'),
    url(r'^search/$', 'search_suggestions',{}),
    url(r'^search/(?P<term>[^/]*)/$', 'search_suggestions',{},'search_suggestions'),
)


