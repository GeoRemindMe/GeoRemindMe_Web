# coding=utf-8 
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

"""
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""


from django.conf.urls.defaults import *
import appengine_admin


urlpatterns = patterns('',
    (r'^(?i)blog/(?P<path>.*)$', 'django.views.generic.simple.redirect_to', {'url': 'http://blog.georemindme.com/%(path)s', 'permanent': True}),
    (r'^(?i)oauth/', include('geoauth.urls')),
    (r'^(?i)ajax/', include('geoajax.urls')),
    (r'^(?i)fb/', include('facebookApp.urls')),
    (r'', include('georpcjson.urls')),
    (r'', include('georemindme.urls')),
    (r'', include('geouser.urls')),
    (r'', include('geoalert.urls')),
)



