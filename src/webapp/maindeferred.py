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

import os, logging, sys
#carga la aplicacion
from google.appengine.ext.webapp import util
from google.appengine.dist import use_library
from google.appengine.ext import deferred
from google.appengine.ext.webapp import template

# elimina cualquier modulo de django cargado (evita conflictos con versiones anteriores)
for k in [k for k in sys.modules if k.startswith('django')]: 
    del sys.modules[k] 
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# carga version 1.2.5 de django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')

import django.core.handlers.wsgi
import django.dispatch
from django.core.signals import got_request_exception
from django.db import _rollback_on_exception

import cPickle, pickle
sys.modules['cPickle'] = sys.modules['pickle']


def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

def main():
    util.run_wsgi_app(deferred.application)

if __name__ == '__main__':
    main() 