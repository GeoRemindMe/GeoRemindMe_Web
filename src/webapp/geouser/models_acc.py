# coding=utf-8

import memcache

from django.utils.translation import gettext_lazy as _
from google.appengine.ext import db

from georemindme.models_utils import *
from georemindme.decorators import classproperty
from signals import user_timeline_new
from models import User

# import code for encoding urls and generating md5 hashes for GRAVATAR
import urllib, hashlib

TIME_CHOICES = ('never', 'instant', 'daily', 'weekly', 'monthly')
class UserSettings(HookedModel):
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
    
    _scgoogleplaces = None
    
    @property
    def searchconfig_google(self):
        if self._scgoogleplaces is None:
            self._scgoogleplaces = SearchConfigGooglePlaces.all().ancestor(self.key()).get()
        return self._scgoogleplaces
    
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
                
    def _post_put(self, **kwargs):
        memcache.set('%s%s' % (memcache.version, self.key().name()), memcache.serialize_instances(self), 300)
        

AVATAR_CHOICES = ('none', 'gravatar', 'facebook', 'twitter')
class UserProfile(HookedModel):
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
            
    def _post_put(self, **kwargs):
        memcache.set('%s%s' % (memcache.version, self.key().name()), memcache.serialize_instances(self), 300)    
    

class UserSocialLinks(HookedModel):
    """Enlaces a los perfiles de redes sociales del usuario"""
    facebook = db.TextProperty(indexed=False)
    twitter = db.TextProperty(indexed=False)
    foursquare = db.TextProperty(indexed=False)
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
    alerts = db.IntegerProperty(default=0)
    followings = db.IntegerProperty(default=0)
    followers = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    
    @classproperty
    def objects(self):
        return UserCounterHelper()
    
    @property
    def supported(self):
        from georemindme.models_utils import ShardedCounter
        return ShardedCounter.get_count('%s_supported'% self.parent().key())
    
    @property
    def influenced(self):
        from georemindme.models_utils import ShardedCounter
        return ShardedCounter.get_count('%s_influenced'% self.parent().key())
    
    def _change_counter(self, prop, value):
        value = int(value)
        obj = UserCounter.get(self.key())
        oldValue = getattr(obj, prop)
        value = oldValue+value
        setattr(obj, prop, value)
        db.put_async(obj)
        return value
        
    def set_suggested(self, value=1):
        return db.run_in_transaction(self._change_counter, 'suggested', value)
    
    def set_alerts(self, value=1):
        return db.run_in_transaction(self._change_counter, 'alerts', value)
    
    def set_supported(self, value=1):
        from georemindme.models_utils import ShardedCounter
        return ShardedCounter.increase_counter('%s_supported'% self.parent().key(), value)
    
    def set_influenced(self, value=1):
        from georemindme.models_utils import ShardedCounter
        return ShardedCounter.increase_counter('%s_influenced'% self.parent().key(), value)
        
    def set_followings(self, value=1):
        return db.run_in_transaction(self._change_counter, 'followings', value)
    
    def set_followers(self, value=1):
        return db.run_in_transaction(self._change_counter, 'followers', value)
    
    
class UserTimelineBase(db.polymodel.PolyModel):
    user = db.ReferenceProperty(User)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        return int(self.key().id())
    

class UserTimelineSystem(UserTimelineBase):
    msg_id = db.IntegerProperty()
    instance = db.ReferenceProperty(db.Model)
    
    @property
    def msg(self):
        _msg_ids = {
                0: _('Welcome to GeoRemindMe you can share your public profile: \
                          <a href="http://www.georemindme.com/user/%(username)s/">\
                          http://www.georemindme.com/user/%(username)s/</a>') %{
                        'username':self.user.username,
                    },
                1: _('Now, you can log with your Google account'),
                2: _('Now, you can log from Facebook and from <a href="http://www.georemindme.com" target="_blank">www.georemindme.com</a>'),
                3: _('Now, you can log with your Twitter account'),
                
                    #User messages
                    100: _('You are now following <a href="%(profile_url)s">%(username)s</a>') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    101: _('<a href="%(profile_url)s">%(username)s</a> is now following you')  % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    102: _('You are no longer following <a href="%(profile_url)s">%(username)s</a> anymore') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    110: _('You invited %s to:') % self.instance,
                    111: _('%s invited you to %s') % (self.instance, self.instance),
                    112: _('%s accepted your invitation to %s') % (self.user, self.instance),
                    113: _('%s rejected your invitation to %s') % (self.user, self.instance),
                    120: _('<a href="%(profile_url)s">%(username)s</a> ha hecho un comentario en la sugerencia: <br><a href="/fb/suggestion/%(suggestion_id)s/">%(suggestion)s</a>') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.user,
                        'suggestion':self.instance,
                        'suggestion_id':self.instance,
                    },
                    125: _('likes a comment: %s') % self.instance,
                    150: _('New user list created: %s') % self.instance,
                    151: _('User list modified: %s') % self.instance,
                    152: _('User list removed: %s') % self.instance,
                    
                    #Alerts
                    200: _('New alert: %s') % self.instance,
                    201: _('Alert modified: %s') % self.instance,
                    202: _('Alert deleted: %s') % self.instance,
                    203: _('Alert done: %s') % self.instance,
                    
                    #Alerts lists
                    250: _('New alert list created: %s') % self.instance,
                    251: _('Alert list modified: %s') % self.instance,
                    252: _('Alert list removed: %s') % self.instance,
                    
                    #Suggestions
                    300: _('<a href="/fb%(url)s">%(username)s</a> sugiere:<br> %(message)s') % {
                        'url':self.user.get_absolute_url(), 
                        'username':self.user.username, 
                        'message':self.instance
                    },
                    301: _('Suggestion modified: %s') % self.instance,
                    302: _('Suggestion removed: %s') % self.instance,
                    303: _('You are following: %s') % self.instance,
                    304: _('You stopped following: %s') % self.instance,
                    305: _('likes a suggestions: %s') % self.instance,
                    320: _('New alert: %s') % self.instance,
                    321: _('Alert modified: %s') % self.instance,
                    322: _('Alert deleted: %s') % self.instance,
                    323: _('Alert done: %s') % self.instance,
                    
                    #Suggestions list
                    350: _('New suggestions list created: %s') % self.instance,
                    351: _('Suggestions list modified: %s') % self.instance,
                    352: _('Suggestion list removed: %s') % self.instance,
                    353: _('You are following: %s') % self.instance,
                    354: _('You are not following %s anymore') % self.instance,
                    
                    #Places
                    400: _('New private place: %s') % self.instance,
                    401: _('Private place modified: %s') % self.instance,
                    402: _('Private place deleted: %s') % self.instance,
                    450: _('New public place: %s') % self.instance,
                    451: _('Public place modified: %s') % self.instance,
                    452: _('Public place deleted: %s') % self.instance,
                }
        return _msg_ids[self.msg_id]

#Equivale al Muro o a los del Perfil
class UserTimeline(UserTimelineBase, Visibility):
    _msg = db.TextProperty(required=False)
    msg_id = db.IntegerProperty(required=False, default=-1)
    instance = db.ReferenceProperty(None)
    
    @property
    def msg(self):
        if self.msg_id != -1:
            _msg_ids = {
                    0: _('Welcome to GeoRemindMe you can share your public profile: \
                          <a href="http://www.georemindme.com/user/%(username)s/">\
                          http://www.georemindme.com/user/%(username)s/</a>') %{
                        'username':self.user.username,
                    },
                    1: _('Now, you can log with your Google account'),
                    2: _('Now, you can log from Facebook and from <a href="http://www.georemindme.com" target="_blank">www.georemindme.com</a>'),
                    3: _('Now, you can log with your Twitter account'),
                    
                    #User messages
                    100: _('You are now following <a href="%(profile_url)s">%(username)s</a>') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    101: _('<a href="%(profile_url)s">%(username)s</a> is now following you')  % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    102: _('You are no longer following <a href="%(profile_url)s">%(username)s</a> anymore') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.instance
                    },
                    110: _('You invited %s to:') % self.instance,
                    111: _('%s invited you to %s') % (self.instance, self.instance),
                    112: _('%s accepted your invitation to %s') % (self.instance, self.instance),
                    113: _('%s rejected your invitation to %s') % (self.instance, self.instance),
                    120: _('<a href="%(profile_url)s">%(username)s</a> ha hecho un comentario en la sugerencia de <a href="%(owner_url)s">%(owner)s</a>: <br><a href="/fb/suggestion/%(suggestion_id)s/">%(suggestion)s</a>') % {
                        'profile_url':self.user.get_absolute_url(),
                        'username':self.user,
                        'owner':self.instance.user,
                        'owner_url':self.instance.user.get_absolute_url(),
                        'suggestion':self.instance,
                        'suggestion_id':self.instance.id,
                    },
                    125: _('likes a comment: %s') % self.instance,
                    150: _('New user list created: %s') % self.instance,
                    151: _('User list modified: %s') % self.instance,
                    152: _('User list removed: %s') % self.instance,
                    
                    #Alerts
                    200: _('New alert: %s') % self.instance,
                    201: _('Alert modified: %s') % self.instance,
                    202: _('Alert deleted: %s') % self.instance,
                    203: _('Alert done: %s') % self.instance,
                    
                    #Alerts lists
                    250: _('New alert list created: %s') % self.instance,
                    251: _('Alert list modified: %s') % self.instance,
                    252: _('Alert list removed: %s') % self.instance,
                    
                    #Suggestions
                    300: _('<a href="/fb%(url)s">%(username)s</a> sugiere:<br> %(message)s') % {
                        'url':self.user.get_absolute_url(), 
                        'username':self.user.username, 
                        'message':self.instance
                    },
                    301: _('Suggestion modified: %s') % self.instance,
                    302: _('Suggestion removed: %s') % self.instance,
                    303: _('You are following: %s') % self.instance,
                    304: _('You stopped following: %s') % self.instance,
                    305: _('likes a suggestions: %s') % self.instance,
                    320: _('New alert: %s') % self.instance,
                    321: _('Alert modified: %s') % self.instance,
                    322: _('Alert deleted: %s') % self.instance,
                    323: _('Alert done: %s') % self.instance,
                    
                    #Suggestions list
                    350: _('New suggestions list created: %s') % self.instance,
                    351: _('Suggestions list modified: %s') % self.instance,
                    352: _('Suggestion list removed: %s') % self.instance,
                    353: _('You are following: %s') % self.instance,
                    354: _('You are not following %s anymore') % self.instance,
                    
                    #Places
                    400: _('New private place: %s') % self.instance,
                    401: _('Private place modified: %s') % self.instance,
                    402: _('Private place deleted: %s') % self.instance,
                    450: _('New public place: %s') % self.instance,
                    451: _('Public place modified: %s') % self.instance,
                    452: _('Public place deleted: %s') % self.instance,
                    }
            return _msg_ids[self.msg_id]
        else:
            return self._msg
    
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
            followers = followers[1]
            page = 1
            while len(followers) > 0:
                page = page+1
                index = UserTimelineFollowersIndex.all().ancestor(self.key()).order('-created').get()
                if index is None or len(index.followers) > 80:  # o no existen indices o hemos alcanzado el maximo
                    index = UserTimelineFollowersIndex(parent=self)
                index.followers.extend(db.Key.from_path(User.kind(), follower['id']) for follower in followers)
                index.put()
                followers = self.user.get_followers(page=page, query_id=query_id)[1]
            return True
    
    @classmethod
    def insert(self, msg, user, instance=None):
        if msg == '' or not isinstance(msg, basestring):
            raise AttributeError()
        timeline = UserTimeline(_msg=msg, user=user, instance=instance)
        timeline.put()
        return timeline
    
    def put(self):
        if self.is_saved():
            super(self.__class__, self).put()
        else:  # si ya estaba guardada, no hay que volver a notificar
            super(self.__class__, self).put()
            user_timeline_new.send(sender=self)
            
    def delete(self):
        query = UserTimelineFollowersIndex.all().ancestor(self.key())
        for timeline in query:
            timeline.delete()
        super(UserTimeline, self).delete()
    

class UserTimelineFollowersIndex(db.Model):
    followers = db.ListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add=True) 


class SearchConfig(db.polymodel.PolyModel):
    region_code = db.TextProperty(default='ES')
    location = db.GeoPtProperty(default='37.175071,-3.598534')
    radius = db.IntegerProperty(default=2000)
    
    
class SearchConfigGooglePlaces(SearchConfig):
    type = db.TextProperty(choices = ('all', 'geocode', 'establishment'), default='establishment')
    
from helpers_acc import *
