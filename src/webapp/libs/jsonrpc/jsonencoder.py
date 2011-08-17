# coding=utf-8

import datetime
import time
from django.utils import simplejson


class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
            #return long(time.mktime(obj.timetuple()))
        from geouser.models import User
        if isinstance(obj, User):
            return obj.to_dict()
        from geoalert.models import Event
        if isinstance(obj, Event):
            return obj.to_dict()
        from geolist.models import List
        if isinstance(obj, List):
            return obj.to_dict()
        from geoalert.models_poi import POI
        if isinstance(obj, POI):
            return obj.to_dict()
        from geovote.models import Comment
        if isinstance(obj, Comment):
            return obj.to_dict()
        from geovote.models import Vote
        if isinstance(obj, Vote):
            return obj.to_dict()
        else:
            return super(self.__class__, self).default(obj)
