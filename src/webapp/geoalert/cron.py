#coding=utf-8


from georemindme.cron import cron_required

from models import Suggestion


@cron_required
def cron_suggestions(request, cursor):
    keys = []
    if cursor is None:
        suggs = Suggestion.all().filter('_vis =', 'public').fetch(500)
    else:
        suggs = Suggestion.all().filter('_vis =', 'public').with_cursor(cursor).fetch(500)
    keys.extend(suggs)
    while len(suggs) == 500:
        keys.extend(suggs)
        q = Suggestion.all().filter('_vis =', 'public').filter('__key__ >', suggs[-1].key())
        suggs = q.fetch(500)
        keys.extend(suggs)
        

    return [x.get_absolute_url() for x in keys]
    from google.appengine.ext.deferred import defer, PermanentTaskFailure 
    try:
        defer(sender.insert_ft, _queue="fusiontables")
    except PermanentTaskFailure, e:
        from georemindme.models_utils import _Do_later_ft
        later = _Do_later_ft(instance_key=sender.key())
        later.put()