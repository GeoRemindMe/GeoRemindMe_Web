from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from protorpc.webapp import service_handlers

from service.api.one import timelineservice, suggestionservice
from service.api import middleware

# Register mapping with application.
application = webapp.WSGIApplication(
                                     service_handlers.service_mapping(
                                          [('/api/1/TimelineService', timelineservice.TimelineService),
                                           ('/api/1/SuggestionService', suggestionservice.SuggestionService)
                                           ]),
                                          debug=True)
#application = middleware.OAuthware(application)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()