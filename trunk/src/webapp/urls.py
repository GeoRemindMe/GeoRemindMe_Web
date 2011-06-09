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
import appengine_admin

from jsonrpc import jsonrpc_site
import georemindme.json_rpc_views

urlpatterns = patterns('',
    # Example:
    (r'^blog/(?P<path>.*)$', 'django.views.generic.simple.redirect_to', {'url': 'http://blog.georemindme.com/%(path)s', 'permanent': True}),
    (r'^oauth/', include('geoauth.urls')),
    #(r'^admin/', include('geoadmin.urls')),
    ##(r'^admin/$', appengine_admin.Admin),
    (r'^ajax/', include('geoajax.urls')),
    url(r'^service/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"),
    (r'', include('georemindme.urls')),
    (r'', include('geouser.urls')),
    (r'', include('geoalert.urls')),
)


