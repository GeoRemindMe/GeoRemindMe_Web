# coding=utf-8

from geouser.decorators import login_forced


@login_forced
def get_suggestions_dict(querier):
    from google.appengine.api import datastore
    q = datastore.Query('Event', {'user =': querier.key()})
    q.Order(('created', datastore.Query.DESCENDING))
    count = q.Count()
    suggs = q.Get(count)
    # separo por tipos
    suggs_following = filter(lambda x: x['class'] == [u'Event', u'AlertSuggestion'], suggs)
    suggs = filter(lambda x: x['class'] == [u'Event', u'Suggestion'], suggs)
    # resolver referencias de AlertSuggestion
    ref_keys = [x['suggestion'] for x in suggs_following]
    suggs_following_resolved = datastore.Get(ref_keys)
    #combinar ambas listas
    suggs.extend(suggs_following_resolved)
    return suggs
    