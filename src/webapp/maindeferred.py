#coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe. If not, see <http://www.gnu.org/licenses/>.

"""

import os, logging, sys
#carga la aplicacion



os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.2')
from django.conf import settings
_ = settings.TEMPLATE_DIRS
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import deferred


application_deferred = deferred.application

def main():
    global application_deferred
    util.run_wsgi_app(application_deferred)

if __name__ == '__main__':
    main()
