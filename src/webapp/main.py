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

# elimina cualquier modulo de django cargado (evita conflictos con versiones anteriores)
for k in [k for k in sys.modules if k.startswith('django')]: 
    del sys.modules[k] 

# carga version 1.2.5 de django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
use_library('django', '1.2')

'''
# Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
  del sys.modules[k]

# Force sys.path to have our own directory first, in case we want to import
# from it.
sys.path.insert(0, 'django.zip')
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
'''

import django.core.handlers.wsgi
import django.dispatch
from django.core.signals import got_request_exception
from django.db import _rollback_on_exception
import cPickle, pickle
sys.modules['cPickle'] = sys.modules['pickle']

def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

# Log errors.
django.dispatch.Signal.connect(
                               got_request_exception,
                               log_exception
                               )

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
                                  got_request_exception,
                                  _rollback_on_exception
                                  )
application = django.core.handlers.wsgi.WSGIHandler()

def main():
    # Create a Django application for WSGI.
    global application
    #application = django.core.handlers.wsgi.WSGIHandler()
    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()

