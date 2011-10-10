#coding=utf-8


from google.appengine.ext.deferred import defer, PermanentTaskFailure 

from django.http import HttpResponse

from georemindme.cron import cron_required
from models import Suggestion


@cron_required
def cron_suggestions(request, cursor=None):
    q = Suggestion.all().filter('_vis =', 'public')
    if cursor is None:
        suggs = q.fetch(500)
    else:
        suggs = q.with_cursor(cursor).fetch(500)
    [s.update_ft() for s in suggs]
    if len(suggs) < 500:
        try:
            defer(cron_suggestions, cursor=q.cursor(), _queue="fusiontables")
        except PermanentTaskFailure, e:
            import logging
            logging.error('ERROR FUSIONTABLES RELEVANCE: %s' % e)
    return HttpResponse()
