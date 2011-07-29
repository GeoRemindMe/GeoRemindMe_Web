# coding=utf-8

"""
.. module:: helpers_acc
    :platform: appengine
    :synopsis: Helpers de los models_acc
"""


class UserSettingsHelper(object):
    def get_by_id(self, userid, async=False):
        try:
            userid = long(userid)
        except:
            return None
        import memcache
        settings = memcache.deserialize_instances(memcache.get('%ssettings_%s' % (memcache.version, userid)))
        if settings is None:
            from models_acc import UserSettings
            from models import User
            from google.appengine.ext import db
            key = db.Key.from_path(User.kind(), userid, UserSettings.kind(), 'settings_%s' % userid)
            settings = db.get(key)
            if settings is not None:
                memcache.set('%s%s' % (memcache.version, settings.key().name()), memcache.serialize_instances(settings), 300)
        return settings

    
class UserProfileHelper(object):
    def get_by_id(self, userid, async=False):
        try:
            userid = long(userid)
        except:
            return None
        import memcache
        profile = memcache.deserialize_instances(memcache.get('%sprofile_%s' % (memcache.version, userid)))
        if profile is None:
            from models_acc import UserProfile
            from models import User
            from google.appengine.ext import db
            key = db.Key.from_path(User.kind(), userid, UserProfile.kind(), 'profile_%s' % userid)
            profile = db.get(key)
            if profile is not None:
                memcache.set('%s%s' % (memcache.version, profile.key().name()), memcache.serialize_instances(profile), 300)
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
        from models_acc import UserCounter
        from models import User
        from google.appengine.ext import db
        key = db.Key.from_path(User.kind(), userid, UserCounter.kind(), 'counters_%s' % userid)
        if async:
            return db.get_async(key)
        return db.get(key)


class UserTimelineHelper(object):
    def get_by_instance_user(self, instance, user):
        from models import User
        if not isinstance(user, User):
            raise TypeError
        from models_acc import UserTimelineBase
        return UserTimelineBase.all().filter('user =', user).filter('instance =', instance).run()

    def get_by_id(self, userid, page=1, query_id = None, querier=None):
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
        from geovote.models import Vote, Comment
        from geoalert.models import Suggestion
        from models_acc import UserTimeline
        from models import User
        from georemindme.paging import PagedQuery
        from google.appengine.ext import db
        q = UserTimeline.all().filter('user =', db.Key.from_path(User.kind(), userid)).order('-created')
        p = PagedQuery(q, id = query_id, page_size=42)
        timelines = p.fetch_page(page)
        if querier is None:
            from models_acc import UserTimelineSystem
            return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'modified': timeline.modified,
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'msg_id': timeline.msg_id,
                        'instance': timeline.instance if timeline.instance is not None else None,
                        'has_voted':  Vote.objects.user_has_voted(db.Key.from_path(User.kind(), userid), timeline.instance.key()) if timeline.instance is not None else None,
                        'vote_counter': Vote.objects.get_vote_counter(timeline.instance.key()) if timeline.instance is not None else None,
                        'comments': Comment.objects.get_by_instance(timeline.instance),
                        'is_private': isinstance(timeline, UserTimelineSystem),
                        } 
                       for timeline in timelines]]
        elif querier.is_authenticated() and querier.are_friends(db.Key.from_path(User.kind(), userid)):
            return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'modified': timeline.modified,
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'msg_id': timeline.msg_id,
                        'instance': timeline.instance if timeline.instance is not None else None,
                        'has_voted':  Vote.objects.user_has_voted(querier, timeline.instance.key()) if timeline.instance is not None else None,
                        'vote_counter': Vote.objects.get_vote_counter(timeline.instance.key()) if timeline.instance is not None else None,
                        'comments': Comment.objects.get_by_instance(timeline.instance, querier=querier),
                        'user_follower': timeline.instance.has_follower(querier) if isinstance(timeline.instance, Suggestion) and querier.is_authenticated() else None,
                        'is_private': False,
                        }
                        for timeline in timelines if timeline._is_shared() or timeline._is_public()]]
        return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'modified': timeline.modified,
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'msg_id': timeline.msg_id,
                        'instance': timeline.instance if timeline.instance is not None else None,
                        'has_voted':  Vote.objects.user_has_voted(querier, timeline.instance.key()) if timeline.instance is not None and querier.is_authenticated()else None,
                        'vote_counter': Vote.objects.get_vote_counter(timeline.instance.key()) if timeline.instance is not None else None,
                        'comments': Comment.objects.get_by_instance(timeline.instance, querier=querier),
                        'user_follower': timeline.instance.has_follower(querier) if isinstance(timeline.instance, Suggestion) and querier.is_authenticated() else None,
                        'is_private': False,
                        }
                       for timeline in timelines if timeline._is_public()]]