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

TIME_CHOICES = ('never', 'instant', 'daily', 'weekly', 'monthly')
class UserSettings(db.Model):
    """Configuracion del usuario (privacidad, etc.)"""
    
    notification_invitation = db.BooleanProperty(indexed=False, default=True)
    notification_list_following = db.BooleanProperty(indexed=False, default=True)
    notification_suggestion_following = db.BooleanProperty(indexed=False, default=True)
    time_notification_suggestion_follower = db.StringProperty(required = True, choices = TIME_CHOICES,
                                                        default = 'weekly')
    time_notification_suggestion_comment = db.StringProperty(required = True, choices = TIME_CHOICES,
                                                        default = 'weekly')
    time_notification_account = db.StringProperty(required = True, choices = TIME_CHOICES,
                                                        default = 'weekly')
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
    
    @property
    def user_id(self):
        return int(self.key().name().split('settings_')[1])

    def notify_follower(self, userkey):
        """
            Manejo de las notificaciones de un usuario
            
                :param user: Usuario que comienza a seguir a self.
                :type user: :class:`geouser.models.User`
        """
        if self.time_notification_account == 'never':
            return
        elif self.time_notification_account == 'instant':
            from geouser.mails import send_notification_follower
            parent = self.parent()
            send_notification_follower(parent.email,
                                       follower=User.objects.get_by_key(userkey),
                                       language=self.language
                                       )
        else:
            from geouser.models_utils import _Report_Account_follower
            _Report_Account_follower.insert_or_update(self.parent().key(), add=userkey)

    def notify_suggestion_follower(self, suggestionkey, userkey):
        if self.time_notification_suggestion_follower == 'never':
            return
        elif self.time_notification_suggestion_follower == 'instant':
            from geouser.mails import send_notification_suggestion_follower
            parent = self.parent()
            from geoalert.models import Suggestion
            send_notification_suggestion_follower(parent.email, 
                                                  suggestion=Suggestion.objects.get_by_key(suggestionkey), 
                                                  user=User.objects.get_by_key(userkey), 
                                                  language=self.language
                                                  )
        else:
            from geouser.models_utils import _Report_Suggestion_changed
            _Report_Suggestion_changed.insert_or_update(self.parent().key(), suggestionkey)
    
           
    def notify_suggestion_comment(self, commentkey):
        if self.time_notification_suggestion_comment == 'never':
            return
        if self.time_notification_suggestion_comment == 'instant':
            from geouser.mails import send_notification_suggestion_comment
            parent = self.parent()
            from geovote.models import Comment
            comment = Comment.objects.get_by_key(commentkey)
            if comment is not None:
                send_notification_suggestion_comment(parent.email,
                                                     comment=comment,
                                                     language=self.language)
        else:
            from geouser.models_utils import _Report_Suggestion_commented
            _Report_Suggestion_commented.insert_or_update(self.parent().key(), comment.instance, comment.created)
                
    def put(self, **kwargs):
        super(UserSettings, self).put()
        memcache.set('%s%s' % (memcache.version, self.key().name()), memcache.serialize_instances(self), 300)
        

AVATAR_CHOICES = ('none', 'gravatar', 'facebook', 'twitter')
class UserProfile(db.Model):
    """Datos para el perfil del usuario"""
    username = db.TextProperty()
    avatar = db.URLProperty(required=False)
    sync_avatar_with = db.StringProperty(required = True, choices = AVATAR_CHOICES,
                                            default = 'gravatar')
    description = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    
    _sociallinks = None
    
    @classproperty
    def objects(self):
        return UserProfileHelper()
    
    @property
    def sociallinks(self):
        if self._sociallinks is None:
            self._sociallinks = UserSocialLinks.all().ancestor(self.key()).get()
        return self._sociallinks
    
    def sociallinks_async(self):
        q = UserSocialLinks.all().ancestor(self.key())
        return q.run()
        
#    def __init__(self, *args, **kwargs):
#        super(self.__class__, self).__init__(*args, **kwargs)

    def _update_gravatar(self):
        parent = self.parent()
        if parent is not None and parent.email is not None:
            email = parent.email
            default = "http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
            size = 50
            # construct the url
            gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            self.avatar = gravatar_url
        
    def _update_facebook(self):
        parent = self.parent()
        if parent.facebook_user is not None:
            self.avatar = "https://graph.facebook.com/%s/picture/" % parent.facebook_user.uid
        else:
            self.avatar = "http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
            
    def put(self):
#        if self.parent().settings.sync_avatar_with_facebook:
#            self._update_facebook()
#        else:
#            self._update_gravatar()
        super(self.__class__, self).put()
        memcache.set('%s%s' % (memcache.version, self.key().name()), memcache.serialize_instances(self),300)    
    

class UserSocialLinks(db.Model):
    """Enlaces a los perfiles de redes sociales del usuario"""
    facebook = db.TextProperty(indexed=False)
    twitter = db.TextProperty(indexed=False)
    foursquares = db.TextProperty(indexed=False)
    created = db.DateTimeProperty(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        from models_social import FacebookUser, TwitterUser
        parent = self.parent().parent()
        facebook = FacebookUser.all().filter('user =', parent).run()
        twitter = TwitterUser.all().filter('user =', parent).run()
        for fb in facebook:
            self.facebook = fb.profile_url
        for tw in twitter:
            self.twitter = 'http://www.twitter.com/%s' % tw.username


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
        
    def set_suggested(self, value=1):
        return db.run_in_transaction(self._change_counter, 'suggested', value)
    
    def set_supported(self, value=1):
        return db.run_in_transaction(self._change_counter, 'supported', value)
    
    def set_influenced(self, value=1):
        return db.run_in_transaction(self._change_counter, 'influenced', value)
    
    def set_followings(self, value=1):
        return db.run_in_transaction(self._change_counter, 'followings', value)
    
    def set_followers(self, value=1):
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
