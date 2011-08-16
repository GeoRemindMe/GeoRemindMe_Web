# coding=utf-8

from django.utils import simplejson
from geoalert.models_poi import *

def getAlertsJSON(alerts):
    """
        Convierte alertas a JSON
        si el tamaño es dos, lo hace de la forma:
            [query_id, alertas)
    """
    from libs.jsonrpc.jsonencoder import JSONEncoder
    if len(alerts) == 3:
        return simplejson.dumps((alerts[0], [a.to_dict() for a in alerts[1]]), int(alerts[2]), cls=JSONEncoder)
    if len(alerts) == 2:
        return simplejson.dumps((alerts[0], [a.to_dict() for a in alerts[1]]), cls=JSONEncoder)
    return alerts[0].to_json()

def getListsJSON(lists):
    if len(lists) == 2:
        from libs.jsonrpc.jsonencoder import JSONEncoder
        return simplejson.dumps((lists[0], [a.to_dict() for a in lists[1]]), cls=JSONEncoder)
    return lists[0].to_json()
