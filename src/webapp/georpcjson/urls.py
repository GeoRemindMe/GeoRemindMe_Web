# coding=utf-8

"""
.. module:: service
    :platform: appengine
    :synopsis: URLs de servicios para movil
"""

from django.conf.urls.defaults import *
from libs.jsonrpc import jsonrpc_site

import georpcjson.views


urlpatterns = patterns('',
       url(r'^(?i)service/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
       #url(r'^(?i)browse/', 'libs.jsonrpc.views.browse', name="jsonrpc_browser"),
)


