# coding=utf-8

from django.utils import simplejson
from geoalert.models_poi import *

def getAlertsJSON(alerts):
    if len(alerts) == 2:
        return simplejson.dumps({'query_id':int(alerts[0]), 'result': [a.to_dict() for a in alerts[1]]})
    return alerts[0].to_json()