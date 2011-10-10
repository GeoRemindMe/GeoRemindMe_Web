#coding=utf-8

import os
#carga la aplicacion
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 
from google.appengine.dist import use_library
use_library('django', '1.2')
from django.conf import settings
_ = settings.TEMPLATE_DIRS


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from protorpc.webapp import service_handlers

from service.api.one import timelineservice, suggestionservice, mapservice, loginservice
from service.api import middleware


# Register mapping with application.
application = webapp.WSGIApplication(
                                     service_handlers.service_mapping(
                                          [('(?i)/api/1/TimelineService', timelineservice.TimelineService),
                                           ('(?i)/api/1/SuggestionService', suggestionservice.SuggestionService),
                                           ('(?i)/api/1/MapService', mapservice.MapService),
                                           ('(?i)/api/1/LoginService', loginservice.LoginService),
                                           ]),
                                          debug=True)
application = middleware.OAuthware(application)

def main():
    global application
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
