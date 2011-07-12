# coding=utf-8
import memcache

from datetime import datetime, timedelta

from django.conf import settings
from django.utils.translation import ugettext as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from georemindme.models_utils import *
from georemindme.funcs import make_random_string
from georemindme.decorators import classproperty
from properties import PasswordProperty, UsernameProperty
from exceptions import *
from signals import *

TIMELINE_PAGE_SIZE = 42


class AnonymousUser(object):
    email = ''
    active = False
   
    def is_authenticated(self):
        return False
    
    def is_admin(self):
        return False


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
            self._google_user = GoogleUser.all().filter('user =', self).get()
        return self._google_user
    
    @property
    def facebook_user(self):
        if self._facebook_user is None:
            self._facebook_user = FacebookUser.all().filter('user =', self).get()
        return self._facebook_user
    
    @property
    def twitter_user(self):
        if self._twitter_user is None:
            self._twitter_user = TwitterUser.all().filter('user =', self).get()
        return self._twitter_user
    
    @property
    def profile(self):
        if self._profile is None:
            #self._profile = memcache.deserialize_instances(memcache.get('%sprofile_%s' % (memcache.version, self.id)))
            #if self._profile is None:
                self._profile = UserProfile.all().ancestor(self.key()).get()
                #memcache.set('%s%s' % (memcache.version, self._profile.key().name()), memcache.serialize_instances(self._profile), 300)
        return self._profile

    @property
    def settings(self):
        if self._settings is None:
            #self._settings = memcache.deserialize_instances(memcache.get('%ssettings_%s' % (memcache.version, self.id)))
            #if self._settings is None:
                self._settings = UserSettings.all().ancestor(self.key()).get() 
                #memcache.set('%s%s' % (memcache.version, self._settings.key().name()), memcache.serialize_instances(self._settings), 300)
        return self._settings
    
    @property
    def counters(self):
        if self._counters is None:
            self._counters = UserCounter.all().ancestor(self.key()).get()
        return self._counters
    

    
    def counters_async(self):
        q = UserCounter.all().ancestor(self.key())
        return q.run()
        
    def get_timelineALL(self, page=1, query_id=None):
        '''
        Obtiene la lista con todos los timeline del usuario

            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''

        q = UserTimelineBase.all().filter('user =', self.key()).order('-created')
        p = PagedQuery(q, id = query_id, page_size=TIMELINE_PAGE_SIZE)
        timelines = p.fetch_page(page)
        return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'instance': timeline.instance if timeline.instance is not None else None }
                        for timeline in timelines]]
        
    def get_timelinesystem(self, page=1, query_id=None):
        '''
        Obtiene la lista de ultimos timelineSystem del usuario

            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        q = UserTimelineSystem.all().filter('user =', self.key()).order('-created')
        p = PagedQuery(q, id = query_id, page_size=TIMELINE_PAGE_SIZE)
        timelines = p.fetch_page(page)
        return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'instance': timeline.instance if timeline.instance is not None else None}
                       for timeline in timelines]]
    
    def get_timeline(self, page=1, query_id=None):
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
        return UserTimeline.objects.get_by_id(self.id)
    
    def get_chronology(self, page=1, query_id=None):
        '''
        Obtiene la lista cronologica con todos los timeline de los usuarios
        a los que sigue este usuario
        
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
        '''
        
        q = db.GqlQuery('SELECT __key__ FROM UserTimelineFollowersIndex WHERE followers = :user', user=self.key())
        p = PagedQuery(q, id = query_id, page_size=TIMELINE_PAGE_SIZE)
        timelines = p.fetch_page(page)
        timelines = [db.get(timeline.parent()) for timeline in timelines]
        return [p.id, [{'id': timeline.id, 'created': timeline.created, 
                        'msg': timeline.msg, 'username':timeline.user.username, 
                        'instance': timeline.instance if timeline.instance is not None else None}
                        for timeline in timelines if timeline is not None ]]
        
        
    def following(self, async=False):
        '''
        Devuelve la lista con todos los indices que el usuario tiene, ordenados por fecha de creacion descendente
        '''
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
    
    """
    @property
    def twitter_user(self):
        return self.twitteruser_set.get()
    """
      
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
        if self.date_remind+timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS) < datetime.now():
            #checks code is in date
            self.date_remind = None
            self.remind_code = None
            raise OutdatedCode()
        if not self.remind_code == code:
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
            settings = UserSettings(key_name='settings_%s' % user.id, parent=user, language=language)
            profile = UserProfile(key_name='profile_%s' % user.id, parent=user, username=user.username, email=user.email)
            followings = UserFollowingIndex(parent=user)
            counters = UserCounter(key_name='counters_%s' % user.id, parent=user)
            sociallinks = UserSocialLinks(parent=profile, key_name='sociallinks_%s' % user.id)
            db.put_async([settings, profile, followings, counters, sociallinks])
            return True
        from django.core.validators import validate_email
        if 'email' in kwargs:
            validate_email(kwargs['email'].decode('utf8'))
        user = User(**kwargs)
        user.put()
        trans = db.run_in_transaction(_tx, user)
        if not trans:
            user.delete()
        from google.appengine.ext.deferred import defer
        user_new.send(sender=user, status=trans)
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
                    logging.debug('Usuario %s email repetido: %s - %s' % (u.id, self.email, u))
                    raise self.UniqueEmailConstraint(self.email)               
        if self.username is not None:
            self.username = self.username.lower()
            u = db.GqlQuery('SELECT __key__ FROM User WHERE username = :1', self.username).get()
            if u is not None:
                if not self.is_saved() or u != self.key(): 
                    logging.debug('Usuario %s username repetido: %s - %s' % (u.id, self.username, u))
                    raise self.UniqueUsernameConstraint(self.username)
    
    def __str__(self):        
        if self.username is None:
            if self.email is None:
                return str(self.id)
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
            if following.id == self.id:
                return True
            is_following = UserFollowingIndex.all().filter('following =', following).ancestor(self.key()).count()
            if is_following != 0:  # en este caso, el usuario ya esta siguiendo al otro, no hacemos nada mas.
                return True
            following_result = self.following(async=True)  # obtiene un iterador con los UserFollowingIndex
            if self._add_follows(following_result, following):
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
            if following.id == self.id:
                return True
            if self._del_follows(following):
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
        try: 
            last_follow = followiterator.next()  # como estan ordenados por fecha de creacion, carga el primero que seria el ultimo indice.
        except StopIteration:
            last_follow = UserFollowingIndex(parent=self)
        if len(last_follow.following) < TIMELINE_PAGE_SIZE*2:  # un maximo de usuarios en este index para que las listas no sean lentas
            last_follow.following.append(key)
        else:  # creamos un index nuevo
            last_follow = UserFollowingIndex(parent=self, following=[key])
        try:
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
        index = UserFollowingIndex.all().ancestor(self.key()).filter('following =', key).get()
        if index is not None:
            index.following.remove(key)
            try:
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
        if UserFollowingIndex.all().ancestor(self.key()).filter('following =', user.key()).count() != 0:
            return True
        return False
    
    def has_follower(self, user=None, userkey=None):
        if userkey is not None:
            if UserFollowingIndex.all().ancestor(userkey).filter('following =', self.key()).count() != 0:
                return True
        elif UserFollowingIndex.all().ancestor(user.key()).filter('following =', self.key()).count() != 0:
            return True
        return False       
    
    def write_timeline(self, msg, instance=None):
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
        
    def get_friends_to_follow(self):
        friends = {}
        from geoauth.clients.facebook import FacebookClient
        try:
            fbclient = FacebookClient(user=self)
            if fbclient.user is not None:
                friends = fbclient.get_friends_to_follow()
        except:
            pass
        try:
            from geoauth.clients.twitter import TwitterClient
            twclient = TwitterClient(user=self)
            if twclient.user is not None:
                friends.update(twclient.get_friends_to_follow())
        except:
            pass
        try:
            from geoauth.clients.google import GoogleClient
            goclient = GoogleClient(user=self)
            if goclient.user is not None:
                friends.update(goclient.get_contacts_to_follow())
        except:
            pass
        return friends
        
from watchers import *
from models_acc import *
from helpers import UserHelper
