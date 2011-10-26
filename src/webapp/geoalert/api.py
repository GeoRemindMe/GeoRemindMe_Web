# coding=utf-8

from geouser.decorators import login_forced
from georemindme import model_plus

from models import Event, Suggestion

@login_forced
def get_suggestions_dict(querier):
    from models_indexes import SuggestionFollowersIndex
    
    indexes = SuggestionFollowersIndex.all(keys_only=True).filter('keys =', querier.key()).order('-created').run()
    suggs = model_plus.fetch_parentsKeys([s for s in indexes])
    if isinstance(suggs, list) and any(suggs):
        suggestions = []
        for s in suggs: # convertir entidades
            setattr(s, 'lists', [])
            suggestions.append(s)
        suggestions = model_plus.prefetch(suggestions, Suggestion.user, Suggestion.poi) 
        return suggestions
    return []


def send_suggestion_to_list(querier, list_id, event_id):
    """
        Un usuario realiza una sugerencia para añadir una sugerencia a una lista
    """
    from google.appengine.api import datastore
    from google.appengine.ext import db
    from geouser.models_acc import UserTimelineSuggest
    from geolist.models import List
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
    timeline = UserTimelineSuggest(instance=keys[1], list=keys[0], user=querier, visible=True)
    timeline.put()
    return True
    
    
def change_suggestion_to_list(querier, timeline_id, status):
    """
        Aceptar o rechazar añadir una sugerencia a una lista
    """
    if not status in (0,1,2):
        return False  
    from google.appengine.api import datastore
    from google.appengine.ext import db
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
        p = datastore.Put(timeline)
    return True


def get_list_from_suggs(s, querier):
    """
        Obtiene las listas de una sugerencia y usuario
    """
    from google.appengine.api import datastore
    q = datastore.Query('List', {'user =': querier.key(), 'list =': s.key()})
    q.Order(('created', datastore.Query.DESCENDING))