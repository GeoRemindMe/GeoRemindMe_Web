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
# Django settings for georemindme project.

from os import path, environ

DEBUG = False
TEMPLATE_DEBUG = DEBUG
BASE_DIR = path.normpath(path.dirname(__file__))

ADMINS = (
    ('Javier Cordero', 'javier@georemindme.com'),
)

MANAGERS = ADMINS

GENERICO = "georemindme"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'af-n%p&_cq(pf)ht6)nss#dpo)+sfj$k$d^l5ltnl$euxxv20w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'django.middleware.common.CommonMiddleware',
    'geomiddleware.facebook.FacebookCSRFMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'geomiddleware.geosessions.geosession',
    'geomiddleware.facebook.FacebookMiddleware',
    'geomiddleware.geolocale.geolocale',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'geomiddleware.geomessages.AJAXMessage',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(BASE_DIR,"templates")
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.humanize',
    'georemindme',
    'geouser',
    'geoalert',
    'geoauth',
    'gaeunit',
    'geotags',
    'georoute',
    'geolist',
    'facebookApp',
    #'libs.jsonrpc',
    'pluginApp',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.csrf',
    'geocontext.context_processors.geoAuth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    #'django.contrib.messages.context_processors.messages',
    
)

LANGUAGES = (
  #~ ('ca', u'Català'),
  #~ ('de', u'Deutsch'),
  ('en', u'English'),
  ('es', u'Español'),
  #~ ('fr', u'Francais'),
  #~ ('gl', u'Galego'),
  #~ ('it', u'Italiano'),
  #~ ('nl', u'Nederlands'),
  #~ ('pl', u'Polski'),
  #~ ('zh', u'Chinese'),
  
)

NO_CONFIRM_ALLOW_DAYS = 7
MAX_ALERTS_PER_PAGE = 15
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

LOGIN_URL = "/"
LOGOUT_URL = "/logout/"
CONTACT_EMAIL = "team@georemindme.com"

MAX_PWD_LENGTH = 12
MIN_PWD_LENGTH = 5

COOKIE_DOMAIN = ''
COOKIE_PATH = '/'
COOKIE_SECURE = True
COOKIE_NAME = 'georemindme_session_cookie'
COOKIE_DATA_NAME = 'georemindme_data_cookie'
COOKIE_SESSION_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600
MAX_SESSION_ID = 18446744073709551616L

OAUTH = {
         'twitter' : {
                      'app_key' : 'SKH1kG4z6lIFNSR8zohhwQ',
                      'app_secret' : 'vViuzQX4H5sn1NDjTTNAZDHH4H2cbNBLPnpyrRf5Q',
                      'request_token_url' : 'https://api.twitter.com/oauth/request_token',
                      'access_token_url' : 'https://api.twitter.com/oauth/access_token',
                      'authorization_url' : 'https://api.twitter.com/oauth/authorize',
                      'authenticate_url' : 'https://api.twitter.com/oauth/authenticate',
                      'callback_url' : 'https://georemindme.appspot.com/oauth/authorized/twitter/',
                      },
         'facebook' : {
                       'app_key': '102408026518300',# APP_ID
                       'app_secret': '1993455d7ed34cbe3cf2d20126dfc014',
                       'realtime_token': '102408026518300|oujl58DaHoE_3DB0zQHC2nRvIVg', # token para acceso REALTIME API
                       'request_token_url' : '',
                       'authorization_url' : 'https://graph.facebook.com/oauth/authorize',
                       'access_token_url' : 'https://graph.facebook.com/oauth/access_token',
                       # Permisos solicitados en la cuenta de Facebook para la App
                       #Lista de permisos disponible en:
                       #http://developers.facebook.com/docs/authentication/permissions/
                       'scope':"email,offline_access,user_likes,user_interests,read_friendlists,user_hometown,publish_stream", 
                       },
          'google' : {
                        'app_key': '74329057869.apps.googleusercontent.com',
                        'app_secret': 'shDMxE0vGC9_E2_ZGOcf0iAa',
                        'request_token_url' : 'https://www.google.com/accounts/OAuthGetRequestToken',
                        'authorization_url' : 'https://www.google.com/accounts/OAuthAuthorizeToken',
                        'access_token_url' : 'https://www.google.com/accounts/OAuthGetAccessToken',
                        'callback_url' : 'http://localhost:8080/oauth/authorized/google/',
                     },
          'yelp' : {
                        'app_key': 'GU34Tmm13DO1l5Br__o1-g',
                        'app_secret': 'gap_JQtQA5tMCiEhN0Rbg3qbwX0',
                        'token_key': 'qN7WTkm6FoosAiHg1FTXno1najLj3KzQ',
                        'token_secret': 'ArE8mc0on3hqZkjvFVMDb9IWs28',
                        
          }
         }

if environ['HTTP_HOST'] == 'localhost:8080':
    OAUTH['facebook']['app_key'] = '170924166301288'
    OAUTH['facebook']['app_secret'] = '14ffcf3c5b16ff78a6ed1506b9a1e555'
    #URL https://apps.facebook.com/georemindme-dev/
    

FACEBOOK_APP = {
         'canvas_name':'georemindme',               # Canvas Page name
         'realtime_verify_token':'RANDOM TOKEN',    # A random token for use with the Real-time API.
         'admin_user_ids':['100002508846747'],       # Facebook User IDs of admins. The poor mans admin system.
}

SHORTENER_ACCESS = {
        'user': 'hhkaos',
        'key': 'aa5a44800923c44a0390cd795ff595e5efc6df7b'
}

if environ['HTTP_HOST'] != 'localhost:8080':
    # The external URL this application is available at where the Real-time 
    # API will send it's pings.p
    WEB_APP='http://georemindme.appspot.com/'
    FACEBOOK_APP['external_href']='http://georemindme.appspot.com/fb/'
    OAUTH['facebook']['callback_url'] = 'https://georemindme.appspot.com/oauth/authorized/facebook/'
    OAUTH['twitter']['callback_url'] = 'https://georemindme.appspot.com/oauth/authorized/twitter/'
else:
    # The external URL this application is available at where the Real-time 
    # API will send it's pings.p
    WEB_APP='http://localhost:8080/'
    FACEBOOK_APP['external_href']='http://localhost:8080/fb/'
    OAUTH['facebook']['callback_url'] = 'http://localhost:8080/oauth/authorized/facebook/'
    OAUTH['twitter']['callback_url'] = 'http://localhost:8080/oauth/authorized/twitter/'


API = {
        'google_places' : 'AIzaSyBWrR-O_l5STwv1EO7U_Y3JNOnVjexf710',
        'google_maps'   : 'ABQIAAAAmy8-KiNfSlxox5XO3XZuaRSH1N1fcQdmTcucWBDBdqkgAa1-PhQNdi8-hO-oo2Jxwbusfuv87fAKHQ',
        'google_maps_secure'   : 'ABQIAAAAmy8-KiNfSlxox5XO3XZuaRRbm4cxlIAzEOiWbFakqGuIogXqIxSbUHIBjJ6fK9mqp7YoPFzOwfQQGQ',
        #'google_maps_production'  : 'ABQIAAAAr-AoA2f89U6keY8jwYAhgRSH1N1fcQdmTcucWBDBdqkgAa1-PhQhWKwe8ygo_Y3tFrHmB0jtJoQ0Bw'
       }

FUSIONTABLES = {
                'token_key': '1/m-5vdnMUSPIe2k9K3bZJa0XR7rvw7FoNkc3Ju4VYSgs',
                'token_secret': 'y354j0CmxUrwUAGmRGvpTbCk',
                'TABLE_PLACES': 1041826 if environ['HTTP_HOST'] == 'localhost:8080' else 1143927,
                'TABLE_SUGGS': 1391263 if environ['HTTP_HOST'] == 'localhost:8080' else 1391270,
                }

    
