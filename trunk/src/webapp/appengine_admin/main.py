from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from appengine_admin.views import Admin

from appengine_admin.model_register import ModelAdmin, register
import appengine_admin.models_admin

application = webapp.WSGIApplication([
    (r'^(/admin)(.*)$', Admin),
])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()