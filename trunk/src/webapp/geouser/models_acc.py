# coding=utf-8

from google.appengine.ext import db

from georemindme.models_utils import Visibility
from georemindme.decorators import classproperty
from models import User


class UserSettings(db.Model):
    """Configuracion del usuario (privacidad, etc.)"""
    notification_followers = db.BooleanProperty(indexed=False, default=True)
    notification_list_following = db.BooleanProperty(indexed=False, default=True)
    notification_suggestion_following = db.BooleanProperty(indexed=False, default=True)
    notification_suggestion_following_comm = db.BooleanProperty(indexed=False, default=True)
    notification_suggestion_comment = db.BooleanProperty(indexed=False, default=True)
    show_followers = db.BooleanProperty(indexed=False, default=True)
    show_followings = db.BooleanProperty(indexed=False, default=True)
    show_timeline = db.BooleanProperty(indexed=False, default=True)
    show_lists = db.BooleanProperty(indexed=False, default=True)
    show_public_profile = db.BooleanProperty(indexed=False, default=True)
    language = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    
    @classproperty
    def objects(self):
        return UserSettingsHelper()
    
    def notify_follower(self, user):
        if self.notification_followers:
            parent= self.parent()
            from geouser.mails import send_notification_follower
            send_notification_follower(parent.email, follower=user)
            
class UserProfile(db.Model):
    """Datos para el perfil del usuario"""
    username = db.TextProperty()
    avatar = db.BlobProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    @classproperty
    def objects(self):
        return UserProfileHelper()
    

class UserSocialLinks(db.Model):
    """Enlaces a los perfiles de redes sociales del usuario"""
    facebook = db.TextProperty(indexed=False)
    twitter = db.TextProperty(indexed=False)
    foursquares = db.TextProperty(indexed=False)
    created = db.DateTimeProperty(auto_now_add=True)


class UserFollowingIndex(db.Model):
    """Listas de gente que sigue el usuario"""
    following = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add=True)
    

class UserCounter(db.Model):
    """Contadores para evitar usar count().
        Podriamos actualizarlos en tiempo real o con algun proceso de background?
    """ 
    suggested = db.IntegerProperty(default=0)
    supported = db.IntegerProperty(default=0)
    influenced = db.IntegerProperty(default=0)
    following = db.IntegerProperty(default=0)
    followers = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    
    @classproperty
    def objects(self):
        return UserCounterHelper()
    
    def _change_counter(self, prop, value):
        obj = UserCounter.get(self.key())
        oldValue = getattr(obj, prop)
        value = oldValue+value
        if value < 0:
            raise ValueError
        setattr(obj, prop, value)
        db.put_async(obj)
        return value
        
    def set_suggested(self, value):
        return db.run_in_transaction(self._change_counter, 'suggested', value)
    
    def set_supported(self, value):
        return db.run_in_transaction(self._change_counter, 'supported', value)
    
    def set_influenced(self, value):
        return db.run_in_transaction(self._change_counter, 'influenced', value)
    
    def set_followings(self, value):
        return db.run_in_transaction(self._change_counter, 'following', value)
    
    def set_followers(self, value):
        return db.run_in_transaction(self._change_counter, 'followers', value)
    
    
class UserTimelineBase(db.polymodel.PolyModel):
    user = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def id(self):
        return int(self.key().id())
    

class UserTimelineSystem(UserTimelineBase):
    msg_id = db.IntegerProperty()
    instance = db.ReferenceProperty(db.Model)
    
    @property
    def msg(self):
        _msg_ids = {
                0: _('Welcome to GeoRemindMe!'),
                100: _('%s is now following you!') % self.instance,
                200: _('New alert: %s') % self.instance,
                300: _('New suggestion: %s') % self.instance,
                350: _('New suggestions list created: %s') % self.instance,
                351: _('Suggestions list modified: %s') % self.instance,
                352: _('Suggestion list removed: %s') % self.instance,
                353: _('Unfollow list: %s') % self.instance,
                }
        return _msg_ids[self.msg_id]

class UserTimeline(UserTimelineBase, Visibility):
    msg = db.TextProperty(required=True)
    instance = db.ReferenceProperty(None)
    
    @classproperty
    def objects(self):
        return UserTimelineHelper()
    
    def __str__(self):
        return '%s - %s' % (self.created.strftime("%B %d, %Y"), self.msg)
    
    def notify_followers(self):
        if not self._is_private():
            if UserTimelineFollowersIndex.all().ancestor(self.key()).count() != 0:
                return True
            followers = self.user.get_followers()
            query_id = followers[0]
            page = 1
            while len(followers) > 0:
                page = page+1
                index = UserTimelineFollowersIndex.all().ancestor(self.key()).order('-created').get()
                if index is None or len(index.followers) > 80:  # o no existen indices o hemos alcanzado el maximo
                    index = UserTimelineFollowersIndex(parent=self)
                index.followers.extend(db.Key.from_path(User.kind(), follower[0]) for follower in followers[1])
                index.put()
                followers = self.user.get_followers(page=page, query_id=query_id)[1]
            return True
    
    def put(self):
        if self.is_saved():
            super(self.__class__, self).put()
        else:  # si ya estaba guardada, no hay que volver a notificar
            super(self.__class__, self).put()
            from georemindme.tasks import NotificationHandler
            NotificationHandler().timeline_followers_notify(self)
    

    
class UserTimelineFollowersIndex(db.Model):
    followers = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add=True) 
    
from helpers_acc import *