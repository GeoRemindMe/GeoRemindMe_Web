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

#geoadmin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^blog/(?P<path>.*)$', 'django.views.generic.simple.redirect_to', {'url': 'http://blog.georemindme.com/%(path)s', 'permanent': True}),
    (r'^oauth/', include('geoauth.urls')),
    #(r'^admin/', include('geoadmin.urls')),
    ##(r'^admin/$', appengine_admin.Admin),
    (r'^ajax/', include('geoajax.urls')),
    (r'', include('georemindme.urls')),
    (r'', include('geouser.urls')),
)

jsonrpc_urlpatterns = patterns('',
    (r'^service/$', 'georemindme.json_rpc_views'),
)

