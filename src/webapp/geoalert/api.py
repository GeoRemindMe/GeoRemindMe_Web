# coding=utf-8

from geouser.decorators import login_forced


@login_forced
def get_suggestions_dict(querier, list_id=None):
    from google.appengine.api import datastore
    q = datastore.Query('Event', {'user =': querier.key()})
    q.Order(('created', datastore.Query.DESCENDING))
    count = q.Count()
    suggs = q.Get(count)
    # separo por tipos
    suggs_following = []
    suggs_cleaned = []
    for s in suggs:
        if 'AlertSuggestion' in s['class']:
            suggs_following.append(s)
        else:
            suggs_cleaned.append(s)
    # resolver referencias de AlertSuggestion
    ref_keys = [x['suggestion'] for x in suggs_following]
    suggs_following_resolved = datastore.Get(ref_keys)
    #combinar ambas listas
    suggs_cleaned.extend(suggs_following_resolved)
    if list_id is not None:
        from google.appengine.ext import db
        list_key = db.Key.from_path('List', int(list_id))
        list = db.get(list_key)
        if list is not None and len(list.keys):
            suggs_cleaned = [s for s in suggs_cleaned if not s.key() in list.keys]
        from geouser.models_acc import UserTimelineSuggest
        keys_suggested = [UserTimelineSuggest.instance.get_value_for_datastore(timeline) for timeline in list.usertimelinesuggest_set]
        suggs_cleaned = [s for s in suggs_cleaned if not s.key() in keys_suggested]
    return suggs_cleaned


def send_suggestion_to_list(querier, list_id, event_id):
    """
        Un usuario realiza una sugerencia para añadir una sugerencia a una lista
    """
    from google.appengine.api import datastore
    from google.appengine.ext import db
    from geouser.models_acc import UserTimelineSuggest
    from geolist.models import List
    from models import Event
    if list_id is None or event_id is None:
        return None
    keys = [db.Key.from_path('List', int(list_id)), db.Key.from_path('Event', int(event_id))] # construir claves
    # no repetimos sugerencias
    q = datastore.Query('UserTimelineBase', {'list =': keys[0], 'instance =': keys[1]})
    if q.Count() != 0:
        return False
    objects = datastore.Get(keys)
    if None in objects:
        return None
    # la sugerencia puede ya estar en la lista
    if objects[0]['user'] == querier.key():
        return False
    try:
        if keys[1] in objects[0]['keys']:
            return False
    except:
        pass
    # creamos la sugerencia
    timeline = UserTimelineSuggest(instance=keys[1], list=keys[0], user=querier, visible=False)
    timeline.put()
    return True
    
    
def change_suggestion_to_list(querier, timeline_id, status):
    if not status in (0,1,2):
        return False  
    from google.appengine.api import datastore
    from geouser.models_utils import _Notification
    from google.appengine.ext import db
    q = datastore.Query('_Notification', {'owner =': querier.key(), 'timeline =': db.Key.from_path('UserTimelineBase', timeline_id)})
    notification = q.Get(1)
    if len(notification) == 0:
        return None
    timeline = datastore.Get(db.Key.from_path('UserTimelineBase', timeline_id))
    if timeline is None:
        return None
    if status == 1:
        list = db.get_async(timeline['list'])
        timeline['status'] = status
        p = datastore.PutAsync(timeline)
        list = list.get_result()
        if list is None:
            return None
        list.update(instances=[timeline['instance'].id()])
        p.get_result()
    else:
        timeline['status'] = status
    return True


def get_list_from_suggs(s, querier):
    from google.appengine.api import datastore
    q = datastore.Query('List', {'user =': querier.key()})
    q.Order(('created', datastore.Query.DESCENDING))