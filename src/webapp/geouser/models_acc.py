# coding=utf-8

import memcache

from django.utils.translation import ugettext as _
from google.appengine.ext import db

from georemindme.models_utils import Visibility
from georemindme.decorators import classproperty
from signals import user_timeline_new
from models import User

# import code for encoding urls and generating md5 hashes for GRAVATAR
import urllib, hashlib

class UserSettings(db.Model):
    """Configuracion del usuario (privacidad, etc.)"""
    notification_invitation = db.BooleanProperty(indexed=False, default=True)
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
            
    def put(self, **kwargs):
        super(UserSettings, self).put()
        memcache.set('%s%s' % (memcache.version, self.key().name()), memcache.serialize_instances(self))
        
            
class UserProfile(db.Model):
    """Datos para el perfil del usuario"""
    username = db.TextProperty()
    avatar = db.URLProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    @classproperty
    def objects(self):
        return UserProfileHelper()
        
    #~ def __init__(self, *args, **kwargs):
        #~ 
        #~ username=kwargs['username']
        #~ #Set your variables here
        #~ if kwargs['parent'].email != '':
            #~ email = kwargs['parent'].email
            #~ default = "http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
            #~ size = 50
            #~ # construct the url
            #~ gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            #~ gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            #~ avatar = gravatar_url
        #~ 
        #~ super(self.__class__, self).__init__(*args, **kwargs)
    

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
    followings = db.IntegerProperty(default=0)
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
        return db.run_in_transaction(self._change_counter, 'followings', value)
    
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
                1: _('Now, you can log with your Google account'),
                2: _('Now, you can log with your Facebook account'),
                3: _('Now, you can log with your Twitter account'),
                100: _('You are now following %s') % self.instance,
                101: _('%s is now following you') % self.instance,
                102: _('You stopped following %s') % self.instance,
                110: _('You invited %s to:') % self.instance,
                111: _('%s invited you to %s') % (self.instance, self.instance),
                150: _('New user list created: %s') % self.instance,
                151: _('User list modified: %s') % self.instance,
                152: _('User list removed: %s') % self.instance,
                200: _('New alert: %s') % self.instance,
                201: _('Alert modified: %s') % self.instance,
                202: _('Alert deleted: %s') % self.instance,
                203: _('Alert done: %s') % self.instance,
                250: _('New alert list created: %s') % self.instance,
                251: _('Alert list modified: %s') % self.instance,
                252: _('Alert list removed: %s') % self.instance,
                300: _('New suggestion: %s') % self.instance,
                301: _('Suggestion modified: %s') % self.instance,
                302: _('Suggestion removed: %s') % self.instance,
                303: _('You are following: %s') % self.instance,
                304: _('You stopped following: %s') % self.instance,
                320: _('New alert: %s') % self.instance,
                321: _('Alert modified: %s') % self.instance,
                322: _('Alert deleted: %s') % self.instance,
                323: _('Alert done: %s') % self.instance,
                350: _('New suggestions list created: %s') % self.instance,
                351: _('Suggestions list modified: %s') % self.instance,
                352: _('Suggestion list removed: %s') % self.instance,
                353: _('You are following: %s') % self.instance,
                354: _('You stopped following: %s') % self.instance,
                400: _('New private place: %s') % self.instance,
                401: _('Private place modified: %s') % self.instance,
                402: _('Private place deleted: %s') % self.instance,
                450: _('New public place: %s') % self.instance,
                451: _('Public place modified: %s') % self.instance,
                452: _('Public place deleted: %s') % self.instance,
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
        if self._is_public():
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
    
    @classmethod
    def insert(self, msg, user, instance=None):
        if msg == '' or not isinstance(msg, basestring):
            raise AttributeError()
        timeline = UserTimeline(msg=msg, user=user, instance=instance)
        timeline.put()
        return timeline
    
    def put(self):
        if self.is_saved():
            super(self.__class__, self).put()
        else:  # si ya estaba guardada, no hay que volver a notificar
            super(self.__class__, self).put()
            user_timeline_new.send(sender=self)
    

class UserTimelineFollowersIndex(db.Model):
    followers = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add=True) 
    
from helpers_acc import *
