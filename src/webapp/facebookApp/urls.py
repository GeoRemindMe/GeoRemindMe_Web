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
from example import *

urlpatterns = patterns('facebookApp.example',
    url(r'^fb/$', 'login_panel'),
    url(r'^fb/dashboard/$', 'dashboard'),
    #url(r'^(?i)timonholandes/$', 'register_panel' ),
    #url(r'^private/', 'homeprivate'),
    #url(r'^team/$',direct_to_template, {'template': 'team.html', 'extra_context': {'active': 'team',}}, 'georemindme.team'),
    #url(r'^(?i)m/$', direct_to_template, {'template': 'mobile/index.html'}, 'georemindme.mobile'),
    #url(r'^(?i)lang/$', 'set_language'),
    #url(r'^(?i)stats/daily/$', 'stats_daily'),
    #url(r'^(?i)clean/sessions/$', 'clean_sessions'),
    #url(r'^(?i)tasks/email/$', 'email_worker'),
    #url(r'^(?i)tasks/notify/timeline/$', 'timelinefollowers_worker'),
    #url(r'^(?i)tasks/notify/list/$', 'list_notify_worker'),
)
