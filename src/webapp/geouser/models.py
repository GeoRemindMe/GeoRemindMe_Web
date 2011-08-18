# coding=utf-8

"""
.. module:: models_acc
    :platform: appengine
    :synopsis: Modelos con los datos relacionados a una cuenta
"""


from django.utils.translation import gettext_lazy as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from georemindme.models_utils import HookedModel
from georemindme.decorators import classproperty
from properties import PasswordProperty, UsernameProperty


TIMELINE_PAGE_SIZE = 10


class AnonymousUser(object):
    email = ''
    active = False

    def is_authenticated(self):
        return False

    def is_admin(self):
        return False

    @property
    def id(self):
        return -1
    
    def key(self):
        return -1


class User(polymodel.PolyModel, HookedModel):
    email = db.EmailProperty()
    username = UsernameProperty()
    password = PasswordProperty(required=True, indexed=False)
    confirm_code = db.TextProperty(indexed=False)
    remind_code = db.TextProperty(indexed=False)
    date_remind = db.DateTimeProperty(indexed=False)
    last_point = db.GeoPtProperty(default=db.GeoPt(37.176487, -3.597929), indexed=False)
    has = db.StringListProperty(default=['active:T', 'confirmed:F', 'admin:F'])
    created = db.DateTimeProperty(auto_now_add=True, indexed=False)
    last_login = db.DateTimeProperty(indexed=False)

    _profile = None
    _settings = None
    _google_user = None
    _twitter_user = None
    _facebook_user = None
    _counters = None


    @classproperty
    def objects(self):
        return UserHelper()

    @property
    def id(self):
        return self.key().id()

    @property
    def google_user(self):
        if self._google_user is None:
            from models_social import GoogleUser
            self._google_user = GoogleUser.all().filter('user =', self).get()
        return self._google_user

    @property
    def facebook_user(self):
        if self._facebook_user is None:
            from models_social import FacebookUser
            self._facebook_user = FacebookUser.all().filter('user =', self).get()
        return self._facebook_user

    @property
    def twitter_user(self):
        if self._twitter_user is None:
            from models_social import TwitterUser
            self._twitter_user = TwitterUser.all().filter('user =', self).get()
        return self._twitter_user

    @property
    def profile(self):
        if self._profile is None:
            import memcache
            self._profile = memcache.deserialize_instances(memcache.get('%sprofile_%s' % (memcache.version, self.id)))
            if self._profile is None:
                from models_acc import UserProfile
                self._profile = UserProfile.all().ancestor(self.key()).get()
                memcache.set('%s%s' % (memcache.version, self._profile.key().name()), memcache.serialize_instances(self._profile), 300)
        return self._profile

    @property
    def settings(self):
        if self._settings is None:
            import memcache
            from models_acc import UserSettings
            self._settings = memcache.deserialize_instances(memcache.get('%ssettings_%s' % (memcache.version, self.id)))
            if self._settings is None:
                self._settings = UserSettings.all().ancestor(self.key()).get()
                memcache.set('%s%s' % (memcache.version, self._settings.key().name()), memcache.serialize_instances(self._settings), 300)
        return self._settings

    @property
    def counters(self):
        if self._counters is None:
            from models_acc import UserCounter
            self._counters = UserCounter.all().ancestor(self.key()).get()
        return self._counters

    def counters_async(self):
        from models_acc import UserCounter
        q = UserCounter.all().ancestor(self.key())
        return q.run()

    def get_profile_timeline(self, query_id=None, querier=None):
        '''
        (Wrapper del metodo UserTimeline.objects.get_by_id(...)
        Obtiene la lista de ultimos timeline publicos del usuario

            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        from models_acc import UserTimeline
        return UserTimeline.objects.get_by_id(self.id, querier=querier, query_id=query_id)

    def get_activity_timeline(self, query_id=None):
        from geouser.models_acc import UserTimelineSystem
        query_chrono = db.GqlQuery('SELECT __key__ FROM UserTimelineFollowersIndex WHERE followers = :user ORDER BY created DESC', user=self.key())
        query_activity = UserTimelineSystem.all().filter('user =', self.key()).filter('visible =', True).order('-modified')
        if query_id is not None and len(query_id)>=2:
            if query_id[0] is not None:  # recuperamos los cursores anteriores
                chrono_id = query_id[0]
                query_chrono = query_chrono.with_cursor(start_cursor=chrono_id)
            if query_id[1] is not None:
                activity_id = query_id[1]
                query_activity = query_activity.with_cursor(start_cursor=activity_id)
        timeline = []
        from geovote.models import Comment, Vote
        from geoalert.models import Event
        from geolist.models import List
        cursor_chronology = None
        cursor_activity = None
        for activity_timeline in query_activity:
            for chrono in query_chrono:
                if len(timeline) >= TIMELINE_PAGE_SIZE:
                        break
                chrono_timeline = db.get(chrono.parent())
                if chrono_timeline.created > activity_timeline.modified:
                    timeline.append({
                                    'id': chrono_timeline.id, 'created': chrono_timeline.created,
                                    'modified': chrono_timeline.modified,
                                    'msg': chrono_timeline.msg, 'username': chrono_timeline.user.username,
                                    'msg_id': chrono_timeline.msg_id,
                                    'instance': chrono_timeline.instance,
                                    'has_voted':  Vote.objects.user_has_voted(self, chrono_timeline.instance.key()) if chrono_timeline.instance is not None else None,
                                    'vote_counter': Vote.objects.get_vote_counter(chrono_timeline.instance.key()) if chrono_timeline.instance is not None else None,
                                    'comments': Comment.objects.get_by_instance(chrono_timeline.instance, querier=self),
                                    'user_follower': chrono_timeline.instance.has_follower(self) if hasattr(chrono_timeline.instance, 'has_follower') else None,
                                    'is_private': False,
                                    })
                    cursor_chronology = query_chrono.cursor()
                else:
                    break
            if len(timeline) >= TIMELINE_PAGE_SIZE:
                break
            timeline.append({
                            'id': activity_timeline.id, 'created': activity_timeline.created,
                            'modified': activity_timeline.modified,
                            'msg': activity_timeline.msg, 'username': activity_timeline.user.username,
                            'msg_id': activity_timeline.msg_id,
                            'instance': activity_timeline.instance,
                            'has_voted':  Vote.objects.user_has_voted(self, activity_timeline.instance.key()) if activity_timeline.instance is not None else None,
                            'vote_counter': Vote.objects.get_vote_counter(activity_timeline.instance.key()) if activity_timeline.instance is not None else None,
                            'comments': Comment.objects.get_by_instance(activity_timeline.instance, querier=self),
                            'is_private': True,
                            })
            query_chrono = query_chrono.with_cursor(start_cursor=cursor_chronology) # avanzamos la consulta hasta el ultimo chronology añadido
            cursor_activity = query_activity.cursor()   
        chronology = [[cursor_chronology, cursor_activity], timeline]
        return chronology

    def get_notifications_timeline(self, query_id=None):
        from models_utils import _Notification
        from geolist.models import List
        query = _Notification.all().filter('owner =', self).order('-_created')
        if query_id is not None:
            query = query.with_cursor(query_id)
        timelines = query.fetch(TIMELINE_PAGE_SIZE)
        return [query.cursor(), [{'id': timeline.id, 'created': timeline.created,
                        'modified': timeline.modified,
                        'msg': timeline.msg, 'username':timeline.user.username,
                        'msg_id': timeline.msg_id,
                        'instance': timeline.instance if timeline.instance is not None else None,
                        'is_private': False,
                        }
                        for timeline in timelines]]

    def following(self, async=False):
        '''
        Devuelve la lista con todos los indices que el usuario tiene, ordenados por fecha de creacion descendente
        '''
        from models_acc import UserFollowingIndex
        if async:
            q = UserFollowingIndex.all().ancestor(self.key()).order('-created')
            return q.run()
        return UserFollowingIndex.all().ancestor(self.key()).order('-created')


    def get_followings(self, page=1, query_id=None):
        '''
        (Wrapper del metodo User.objects.get_followings(...)
        Obtiene la lista de personas a las que sigue el usuario

            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username)
        '''
        return self.objects.get_followings(userid=self.id, page=page, query_id=query_id)

    def get_followers(self, page=1, query_id=None):
        '''
        (Wrapper del metodo User.objects.get_followers(...)
        Obtiene la lista de personas que siguen al usuario

            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username)
        '''
        return self.objects.get_followers(userid=self.id, page=page, query_id=query_id)

    def get_friends(self):
        from models_acc import UserFollowingIndex
        indexes = UserFollowingIndex.all().ancestor(self.key())
        # cargo la lista completa de todos a los que sigue el usuario
        followings = []
        followings.extend([following for index in indexes for following in index.following])
        friends = []
        for follow in followings:
            key = db.GqlQuery('SELECT __key__ FROM UserFollowingIndex WHERE ANCESTOR IS :1 AND following =:2', follow, self.key()).get()
            if key is not None:
                friends.append(follow)
        return db.get_async(friends)

    def are_friends(self, friend):
        from models_acc import UserFollowingIndex
        if isinstance(friend, db.Key):
            user_following = UserFollowingIndex.all().filter('following =', friend).ancestor(self.key()).count()
            if user_following == 0:
                return False
            friend_following = UserFollowingIndex.all().filter('following =', self.key()).ancestor(friend).count()
            if friend_following == 0:
                return False
        else:
            user_following = UserFollowingIndex.all().filter('following =', friend.key()).ancestor(self.key()).count()
            if user_following == 0:
                return False
            friend_following = UserFollowingIndex.all().filter('following =', self.key()).ancestor(friend.key()).count()
            if friend_following == 0:
                return False
        return True

    def is_authenticated(self):
        return True

    def is_active(self):
        if 'active:T' in self.has:
            return True
        return False

    def is_confirmed(self):
        if 'confirmed:T' in self.has:
            return True
        return False

    def is_admin(self):
        if 'admin:T' in self.has:
            return True
        return False

    def get_language(self):
        return self.settings.language

    def toggle_active(self):
        if self.is_active():
            self.has.remove('active:T')
            self.has.append('active:F')
            return False
        self.has.remove('active:F')
        self.has.append('active:T')
        return True

    def toggle_confirmed(self):
        if self.is_confirmed():
            self.has.remove('confirmed:T')
            self.has.append('confirmed:F')
            return False
        self.has.remove('confirmed:F')
        self.has.append('confirmed:T')
        return True

    def toggle_admin(self):
        if self.is_admin():
            self.has.remove('admin:T')
            self.has.append('admin:F')
            return False
        self.has.remove('admin:F')
        self.has.append('admin:T')
        return True

    def check_password(self, raw):
        '''
            Comprueba que el password es el correcto
        '''
        raw = str(raw)
        alg, seed, passw = self.password.split('$')
        from django.utils.hashcompat import sha_constructor
        return passw == sha_constructor(seed + raw).hexdigest()

    def send_confirm_code(self, commit = True):
        '''
            Envia un correo de confirmacion de direccion de correo
        '''
        if self.email == '' or self.email is None:
            return None
        if not self.is_confirmed():
            from georemindme.funcs import make_random_string
            self.confirm_code = make_random_string(length=24)
            if commit:
                self.put()
            from geouser.mails import send_confirm_mail
            send_confirm_mail(self.email, self.confirm_code, language=self.get_language())  # send mail

    def confirm_user(self, code):
        """Confirms the user"""
        if self.confirm_code == code:
            self.toggle_confirmed()
            self.put()
            return True
        return False

    def send_remind_code(self):
        '''
        Envia un correo con un codigo para iniciar la recuperacion de contraseña
        '''
        if self.email == '' or self.email is None:
            return None
        from georemindme.funcs import make_random_string
        self.remind_code = make_random_string(length=24)
        from datetime import datetime
        self.date_remind = datetime.now()
        self.put()
        from geouser.mails import send_remind_pass_mail
        send_remind_pass_mail(self.email, self.remind_code, language=self.get_language())#send mail

    def reset_password(self, code, password=None):
        '''
        Resetea el password del usuario si el codigo es correcto

            :param user: The user
            :type user: :class:`User`
            :param code: remind code
            :type code: string
            :returns: boolean
            :raises: OutdatedCode, BadCode
        '''
        from datetime import datetime, timedelta
        from django.conf import settings
        if self.date_remind+timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS) < datetime.now():
            #checks code is in date
            self.date_remind = None
            self.remind_code = None
            from exceptions import OutdatedCode
            raise OutdatedCode()
        if not self.remind_code == code:
            from exceptions import BadCode
            raise BadCode()
        if password is not None:
            self.password = password
            self.remind_code = None
            self.date_remind = None
            self.put()
        return True

    @classmethod
    def register(cls, language='en', **kwargs):
        '''
        Registra un nuevo usuario, crea todas las instancias hijas necesarias

            :returns: :class:`geouser.models.User`
            :raises: :class:`UniqueEmailConstraint` si el email ya esta en uso
            :raise: :class:`UniqueUsernameConstraint` si el username ya esta en uso
        '''
        def _tx(user):
            try:
                from models_acc import UserFollowingIndex, UserSettings, UserProfile, UserCounter
                settings = UserSettings(key_name='settings_%s' % user.id, parent=user, language=language)
                profile = UserProfile(key_name='profile_%s' % user.id, parent=user, username=user.username, email=user.email)
                followings = UserFollowingIndex(parent=user)
                counters = UserCounter(key_name='counters_%s' % user.id, parent=user)
                db.put_async([settings, profile, followings, counters])
                return True
            except:
                return False
        from django.core.validators import validate_email
        if 'email' in kwargs:
            validate_email(kwargs['email'].decode('utf8'))
        user = User(**kwargs)
        user.put()
        trans = db.run_in_transaction(_tx, user)
        if not trans:
            user.delete()
        else:
            from models_acc import UserSocialLinks, SearchConfigGooglePlaces
            sociallinks = UserSocialLinks(parent=user.profile, key_name='sociallinks_%s' % user.id)
            scgoogleplaces = SearchConfigGooglePlaces(parent=user.settings, key_name='searchgoogle_%d' % user.id)
            save = db.put_async([sociallinks, scgoogleplaces])
            from google.appengine.ext.deferred import defer
            from signals import user_new
            user_new.send(sender=user, status=trans)
            save.get_result()
            return user

    def update(self, **kwargs):
        '''
        Actualiza los datos de identificacion de un usuario, el nombre de usuario tambien se guarda en UserProfile,
        por lo que hay que actualizarlo tambien
        '''
        backemail = self.email
        backusername = self.username
        backpassword = self.password

        if 'email' in kwargs:
            if self.email != kwargs['email']:
                from django.core.validators import validate_email
                validate_email(kwargs['email'])
                self.email = kwargs['email']
        if 'username' in kwargs:
            self.username = kwargs['username']
            self.profile.username = self.username
        if 'password' in kwargs:
            self.password = kwargs['password']
        if 'description' in kwargs:
            self.profile.description = kwargs['description']
        if 'sync_avatar_with' in kwargs:
            self.profile.sync_avatar_with = kwargs['sync_avatar_with']
        try:
            put = db.put_async([self, self.profile])
            put.get_result()
        except:
            self.email = backemail
            self.username = backusername
            self.password = backpassword
            raise
        return self

    def _pre_put(self):
        # Ensure that email is unique
        if self.email is not None:
            self.email = self.email.lower()
            u = db.GqlQuery('SELECT __key__ FROM User WHERE email = :1', self.email).get()
            if u is not None:
                if not self.is_saved() or u != self.key():
                    import logging
                    logging.debug('Usuario %s email repetido: %s - %s' % (u.id, self.email, u))
                    raise self.UniqueEmailConstraint(self.email)
        if self.username is not None:
            self.username = self.username.lower()
            u = db.GqlQuery('SELECT __key__ FROM User WHERE username = :1', self.username).get()
            if u is not None:
                if not self.is_saved() or u != self.key():
                    import logging
                    logging.debug('Usuario %s username repetido: %s - %s' % (u.id, self.username, u))
                    raise self.UniqueUsernameConstraint(self.username)

    def __str__(self):
        if self.username is None:
            if self.email is None:
                return unicode(self.id)
            return unicode(self.email).encode('utf-8')
        return unicode(self.username).encode('utf-8')

    def __unicode__(self):
        if self.username is None:
            if self.email is None:
                return unicode(self.id)
            return self.email
        return self.username

    def add_following(self, followname = None, followid = None):
        '''
        Añade un usuario a la lista de personas que sigue self.
        El usuario se busca a por username o por id

            :param followname: El nombre de usuario a seguir
            :type followname: :class:`string`
            :param followid: El identificador del usuario a seguir
            :type followid: :class:`string`
        '''
        if followname is not None:
            following = User.objects.get_by_username(followname, keys_only=True)
        elif followid is not None:
            following = User.objects.get_by_id(followid, keys_only=True)
        else:
            raise AttributeError()
        if following is not None:
            if following == self.key():
                return True
            import memcache
            friends = memcache.get('%sfriends_to_%s' % (memcache.version, self.key()))
            if friends is not None and int(following.id()) in friends:
                del friends[int(following.id())]
                memcache.set('%sfriends_to_%s' % (memcache.version, self.key()), friends, 300)
            from models_acc import UserFollowingIndex
            is_following = UserFollowingIndex.all().filter('following =', following).ancestor(self.key()).count()
            if is_following != 0:  # en este caso, el usuario ya esta siguiendo al otro, no hacemos nada mas.
                return True
            following_result = self.following(async=True)  # obtiene un iterador con los UserFollowingIndex
            if self._add_follows(following_result, following):
                from signals import user_follower_new
                user_follower_new.send(sender=self, following=following)
                return True
        return False

    def del_following(self, followname = None, followid = None):
        '''
        Borra un usuario de la lista de following
        El usuario se busca a por username o por id

            :param followname: El nombre de usuario a seguir
            :type followname: :class:`string`
            :param followid: El identificador del usuario a seguir
            :type followid: :class:`string`
        '''
        if followname is not None:
            if followname == self.username:
                return False
            following = User.objects.get_by_username(followname, keys_only=True)
        elif followid is not None:
            if followid == self.id:
                return False
            following = User.objects.get_by_id(followid, keys_only=True)
        else:
            raise AttributeError()
        if following is not None:
            if following == self.key():
                return True
            if self._del_follows(following):
                from signals import user_following_deleted
                user_following_deleted.send(sender=self, following=following)
                return True
        return False


    def _add_follows(self, followiterator, key):
        '''
            Guarda el usuario en el ultimo index posible, si se ha llegado al maximo
            numero de usuarios por lista, se crea uno nuevo.

            :param followiterator: Iterador con la consulta para obtener los index, ordenador por fecha de creacion
                asi el primero de la lista, sera el ultimo index posible.
            :type followiterator: :class:`_QueryIterator`
            :param key: key del usuario a añadir
            :type key: :class:`db.Key()
            :returns: True si se añadio el usuario
        '''
        from models_acc import UserFollowingIndex
        try:
            last_follow = followiterator.next()  # como estan ordenados por fecha de creacion, carga el primero que seria el ultimo indice.
        except StopIteration:
            last_follow = UserFollowingIndex(parent=self)
        if len(last_follow.following) < TIMELINE_PAGE_SIZE*2:  # un maximo de usuarios en este index para que las listas no sean lentas
            last_follow.following.append(key)
        else:  # creamos un index nuevo
            last_follow = UserFollowingIndex(parent=self, following=[key])
        try:
            from models_acc import UserCounter
            counter_result = self.counters_async() # obtiene los contadores de self
            follow_query = UserCounter.all().ancestor(key) # obtiene los contadores del otro usuario
            follow_result = follow_query.run()
            counter_result = counter_result.next()
            follow_result = follow_result.next()
            counter_result.set_followings(+1) # sumamos uno al contador de following
            follow_result.set_followers(+1)# sumamos uno al contador de followers del otro usuario
        except:
            return False
        last_follow.put()
        return True

    def _del_follows(self, key):
        '''
            Borra un key de la lista de following

            :param key: key del usuario a borrar
            :type key: :class:`db.Key()
            :returns: True si se borro el usuario, False si no se encontro
        '''
        from models_acc import UserFollowingIndex
        index = UserFollowingIndex.all().ancestor(self.key()).filter('following =', key).get()
        if index is not None:
            index.following.remove(key)
            try:
                from models_acc import UserCounter
                counter_result = self.counters_async() # obtiene los contadores de self
                follow_query = UserCounter.all().ancestor(key) # obtiene los contadores del otro usuario
                follow_result = follow_query.run()
                counter_result = counter_result.next()
                follow_result = follow_result.next()
                counter_result.set_followings(-1) # sumamos uno al contador de following
                follow_result.set_followers(-1) # sumamos uno al contador de followers del otro usuario
            except:
                return False
            index.put()
            return True
        return False

    def is_following(self, user):
        from models_acc import UserFollowingIndex
        if UserFollowingIndex.all().ancestor(self.key()).filter('following =', user.key()).count() != 0:
            return True
        return False

    def has_follower(self, user=None, userkey=None):
        from models_acc import UserFollowingIndex
        if userkey is not None:
            if UserFollowingIndex.all().ancestor(userkey).filter('following =', self.key()).count() != 0:
                return True
        elif not user.is_authenticated():
            return False
        elif UserFollowingIndex.all().ancestor(user.key()).filter('following =', self.key()).count() != 0:
            return True
        return False

    def write_timeline(self, msg, instance=None):
        from models_acc import UserTimeline
        return UserTimeline.insert(msg=msg, user=self, instance=instance)

    def delete_async(self):
        children = db.query_descendants(self).fetch(10)
        for c in children:
            c.delete()
        return db.delete_async(self)

    class UniqueEmailConstraint(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return _('Email already in use: %s') % self.value

    class UniqueUsernameConstraint(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return _('Username already in use: %s') % self.value

    def get_absolute_url(self):
        if self.username is not None:
            return '/user/%s/' % str(self.username)

    def get_absolute_fburl(self):
        return '/fb%s' % self.get_absolute_url()

    def get_friends_to_follow(self):
        import memcache
        friends = memcache.get('%sfriends_to_%s' % (memcache.version, self.key()))
        if friends is None:
            friends = {}
            from geoauth.clients.facebook import FacebookClient
            try:
                fbclient = FacebookClient(user=self)
                friends.update(fbclient.get_friends_to_follow())
            except:
                pass
            try:
                from geoauth.clients.twitter import TwitterClient
                twclient = TwitterClient(user=self)
                friends.update(twclient.get_friends_to_follow())
            except:
                pass
            try:
                from geoauth.clients.google import GoogleClient
                goclient = GoogleClient(user=self)
                friends.update(goclient.get_contacts_to_follow())
            except:
                pass
            if len(friends) > 0:
                if len(self.settings.blocked_friends_sug)>0:
                    for k in friends.keys():
                        if k in self.settings.blocked_friends_sug:
                            del friends[k]
                memcache.set('%sfriends_to_%s' % (memcache.version, self.key()), friends, 300)
        return friends

    def to_dict(self):
        return {
                'id': self.id,
                'username': self.username,
                'get_absolute_url': self.get_absolute_url(),
                'get_absolute_fburl': self.get_absolute_fburl(),
                }

from helpers import UserHelper
from watchers import *
