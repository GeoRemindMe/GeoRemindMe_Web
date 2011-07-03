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

import facebookApp.watchers
#~ from facebookApp import 

urlpatterns = patterns('facebookApp.views',
    url(r'^fb/$', 'login_panel'),
    url(r'^fb/dashboard/$', 'dashboard'),
    url(r'^fb/profile/$', 'profile_settings'),
    url(r'^fb/user/(?P<username>\w+)$', 'user_profile'),
    url(r'^fb/user/(?P<username>\w+)/followers/$', 'followers_panel'),
    url(r'^fb/user/(?P<username>\w+)/followings/$', 'followings_panel'),
    url(r'^fb/suggestions/$', 'user_suggestions'),
)
