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
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('georemindme.views',
    url(r'login/$', 'private_home', {'login':True} ),
    url(r'timonholandes/$', 'home' ),
    #url(r'^private/', 'homeprivate'),
    url(r'^dashboard/$', 'dashboard'),
    url(r'^logout/$', 'logout'),
    #url(r'^team/$',direct_to_template, {'template': 'team.html', 'extra_context': {'active': 'team',}}, 'georemindme.team'),
    url(r'^m/$', direct_to_template, {'template': 'mobile/index.html'}, 'georemindme.mobile'),
    url(r'^contact/$', direct_to_template, {'template': 'webapp/contact.html'}, 'contact'),
    url(r'^privacy/$', direct_to_template, {'template': 'webapp/privacypolicy.html'}, 'privacy'),
    url(r'^tos/$', direct_to_template, {'template': 'webapp/tos.html'}, 'tos'),
    url(r'^knowmore/$', direct_to_template, {'template': 'webapp/knowmore.html'}, 'knowmore'),
    url(r'^sitemap.xml', direct_to_template, {'template': 'webapp/sitemap.xml'}, 'sitemap'),
    url(r'^confirm/(?P<user>[^/]*)/(?P<code>[^/]*)/$', 'confirm', {}, 'georemidme.confirm'),
    url(r'^lang/$', 'set_language'),
    url(r'^demo/$', 'demo'),
    url(r'^$', 'private_home'),
    #url(r'^login/google/$','login_google', {}, 'georemidme.login_google'),
    #url(r'^remindpass/$','remind_user', {}, 'georemidme.remind_user'),
    #url(r'^remindpass/(?P<user>[^/]*)/(?P<code>[^/]*)/$','remind_user_pass', {}, 'georemidme.remind_pass'),
    #url(r'^json/$', 'json'),
)


