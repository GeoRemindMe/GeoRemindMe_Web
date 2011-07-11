# coding=utf-8

from google.appengine.ext import db

from models_acc import *
from models import User
from georemindme.paging import *
import memcache


class UserSettingsHelper(object):
    def get_by_id(self, userid, async=False):
        try:
            userid = long(userid)
        except:
            return None
        settings = memcache.deserialize_instances(memcache.get('%ssettings_%s' % (memcache.version, userid)))
        if settings is None:
            key = db.Key.from_path(User.kind(), userid, UserSettings.kind(), 'settings_%s' % userid)
            settings = db.get(key)
            memcache.set('%s%s' % (memcache.version, settings.key().name()), memcache.serialize_instances(settings))
        return settings
        """
        if async:
            return db.get_async(key)
        return db.get(key)
        """
    
class UserProfileHelper(object):
    def get_by_id(self, userid, async=False):
        try:
            userid = long(userid)
        except:
            return None
        profile = memcache.deserialize_instances(memcache.get('%sprofile_%s' % (memcache.version, userid)))
        if profile is None:
            key = db.Key.from_path(User.kind(), userid, UserProfile.kind(), 'profile_%s' % userid)
            profile = db.get(key)
            memcache.set('%s%s' % (memcache.version, profile.key().name()), memcache.serialize_instances(profile))
        return profile
        """
        if async:
            return db.get_async(key)
        return db.get(key)
        """

class UserCounterHelper(object):
    def get_by_id(self, userid, async=False):
        try:
            userid = long(userid)
        except:
            return None
        key = db.Key.from_path(User.kind(), userid, UserCounter.kind(), 'counters_%s' % userid)
        if async:
            return db.get_async(key)
        return db.get(key)
    
class UserTimelineHelper(object):
    def get_by_id(self, userid, page=1, query_id = None, vis='public'):
        '''
        Obtiene la lista de ultimos timeline del usuario

            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        try:
            userid = long(userid)
        except:
            return None
        q = UserTimeline.all().filter('user =', db.Key.from_path(User.kind(), userid)).order('-created')
        p = PagedQuery(q, id = query_id, page_size=42)
        timelines = p.fetch_page(page)
        if vis.lower()=='public':
            return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                            'msg': timeline.msg, 'username':timeline.user.username, 
                            'instance': timeline.instance if timeline.instance is not None else None} 
                           for timeline in timelines if timeline._is_public()]]
        if vis.lower()=='shared':
            return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                            'msg': timeline.msg, 'username':timeline.user.username, 
                            'instance': timeline.instance if timeline.instance is not None else None}
                            for timeline in timelines if timeline._is_shared() or timeline._is_public()]]
