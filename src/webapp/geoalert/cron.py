#coding=utf-8


from google.appengine.ext.deferred import defer, PermanentTaskFailure 

from django.http import HttpResponse

from georemindme.cron import cron_required
from models import Suggestion


@cron_required
def cron_suggestions(request, cursor=None):
    q = Suggestion.all().filter('_vis =', 'public')
    if cursor is None:
        suggs = q.fetch(50)
    else:
        suggs = q.with_cursor(cursor).fetch(50)
    if len(suggs) >= 50:
        try:
            defer(cron_suggestions, request, cursor=q.cursor(), _queue="fusiontables")
        except PermanentTaskFailure, e:
            import logging
            logging.error('ERROR FUSIONTABLES update relevance: %s' % e)
    [s.update_ft() for s in suggs]
    return HttpResponse()

