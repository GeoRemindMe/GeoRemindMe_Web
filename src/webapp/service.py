#coding=utf-8

import os
#carga la aplicacion
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 

import webapp2
from protorpc.webapp import service_handlers

from service.api.one import timelineservice, suggestionservice, mapservice, loginservice
from service.api import middleware


# Register mapping with application.
app = webapp2.WSGIApplication(
                                     service_handlers.service_mapping(
                                          [('(?i)/api/1/TimelineService', timelineservice.TimelineService),
                                           ('(?i)/api/1/SuggestionService', suggestionservice.SuggestionService),
                                           ('(?i)/api/1/MapService', mapservice.MapService),
                                           ('(?i)/api/1/LoginService', loginservice.LoginService),
                                           ]),
                                          debug=True)
app = middleware.OAuthware(app)
