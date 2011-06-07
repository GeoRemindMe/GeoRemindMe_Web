# coding=utf-8
import logging

from datetime import datetime, timedelta

from django.conf import settings
from django.utils.translation import ugettext as _
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

from georemindme.models_utils import Counter
from georemindme.funcs import make_random_string
from properties import PasswordProperty, UsernameProperty
from exceptions import *

from georemindme.decorators import classproperty
import memcache

TIMELINE_PAGE_SIZE = 42

class User(polymodel.PolyModel):
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
    
    @classproperty
    def objects(self):
        return UserHelper()
    
    @property
    def id(self):
        return self.key().name()
    
    @property
    def profile(self):
        if self._profile is None:
            self._profile = memcache.deserialize_instances(memcache.get('%s%s_profile' % (memcache.version, id)))
            if self._profile is None:
                self._profile = UserProfile.all().ancestor(self.key()).get()
                memcache.set('%s%s_profile' % (memcache.version, id), memcache.serialize_instances(self._profile))
        return self._profile

    @property
    def settings(self):
        if self._settings is None:
            self._settings = memcache.deserialize_instances(memcache.get('%s%s_settings' % (memcache.version, id)))
            if self._settings is None:
                self._settings = UserSettings.all().ancestor(self.key()).get() 
                memcache.set('%s%s_settings' % (memcache.version, id), memcache.serialize_instances(self._settings))
        return self._settings
        
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
        return [p.id, [(timeline.id, timeline.created, timeline.user.username, timeline.msg, timeline.instance.key() if timeline.instance is not None else None) for timeline in timelines]]
        
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
        return [p.id, [(timeline.id, timeline.created, timeline.user.username, timeline.msg, timeline.instance.key() if timeline.instance is not None else None) for timeline in timelines]]
    
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
        return [p.id, [(timeline.id, timeline.user.username, timeline.msg) for timeline in timelines]]
        
        
    def following(self, async=False):
        '''
        Devuelve la lista con todos los indices que el usuario tiene, ordenados por fecha de creacion descendente
        '''
        if async:
            q = UserFollowingIndex.all().ancestor(self.key()).order('-created')
            return q.run()
        return UserFollowingIndex.all().ancestor(self.key()).order('-created')
        
    def counters(self, async=False):
        if async:
            q = UserCounter.all().ancestor(self.key())
            return q.run()
        return UserCounter.all().ancestor(self.key()).get()
    
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
        alg, seed, passw = self.password.split('$')
        from django.utils.hashcompat import sha_constructor
        return passw == sha_constructor(seed + raw).hexdigest()
    
    def send_confirm_code(self, commit = True):
        '''
            Envia un correo de confirmacion de direccion de correo
        '''
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
            settings = UserSettings(key_name='%s_settings' % user.key().name(), parent=user, language=language)
            profile = UserProfile(key_name='%s_profile' % user.key().name(), parent=user, nickname=user.username)
            followings = UserFollowingIndex(parent=user)
            counters = UserCounter(key_name='%s_counters' % user.key().name(), parent=user)
            sociallinks = UserSocialLinks(parent=profile)
            db.put_async([settings, profile, followings, counters, sociallinks])
        key_name = 'u%d' % Counter.get_counter('User')
        user = User(key_name=key_name, **kwargs)
        user.put()
        db.run_in_transaction(_tx, user)
        timeline = UserTimelineSystem(user = user, msg_id=0)
        timeline.put()
        logging.info('Registrado nuevo usuario %s email: %s' % (user.id, user.email))

        return user
    
    def update(self, **kwargs):
        '''
        Actualiza los datos de identificacion de un usuario, el nombre de usuario tambien se guarda en UserProfile,
        por lo que hay que actualizarlo tambien
        '''
        profile = None
        if 'email' in kwargs:
            if self.email != kwargs['email']:
                self.email = kwargs['email']
                self.send_confirm_code(commit=False)
        if 'username' in kwargs:
            self.username = kwargs['username']
            self.profile.username = self.username
        put = db.put_async([self, self.profile])
        put.get_result()
        return self
    
    def put(self):
        # Ensure that email is unique
        if self.email is not None:
            self.email = self.email.lower()
            u = db.GqlQuery('SELECT __key__ FROM User WHERE email = :1', self.email).get()
            if u is not None:
                if not self.is_saved() or u != self.key(): 
                    logging.debug('Usuario %s email repetido: %s - %s' % (self.id, self.email, u))
                    raise self.UniqueEmailConstraint(self.email)               
        if self.username is not None:
            self.username = self.username.lower()
            u = db.GqlQuery('SELECT __key__ FROM User WHERE username = :1', self.username).get()
            if u is not None:
                if not self.is_saved() or u != self.key(): 
                    logging.debug('Usuario %s username repetido: %s - %s' % (self.id, self.username, u))
                    raise self.UniqueUsernameConstraint(self.username)
        super(self.__class__, self).put()
        
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
        is_following = UserFollowingIndex.all().filter('following =', following).ancestor(self.key()).count()
        if is_following != 0:  # en este caso, el usuario ya esta siguiendo al otro, no hacemos nada mas.
            return True
        #probando las busquedas asincronas
        following_result = self.following(async=True)  # obtiene un iterador con los UserFollowingIndex
        counter_result = self.counters(async=True) # obtiene los contadores de self
        follow_query = UserCounter.all().ancestor(following) # obtiene los contadores del otro usuario
        follow_result = follow_query.run()
        settings_follow_query = UserSettings.all().ancestor(following)
        settings_follow_result = settings_follow_query.run()
        added = self._add_follows(following_result, following)
        if added:
            counter_result = counter_result.next()  # sumamos uno al contador de following
            follow_result = follow_result.next()
            counter_result.set_followings(+1)
            # sumamos uno al contador de followers del otro usuario
            follow_result.set_followers(+1)
            settings_follow_result.next().notify_follower(self)  # mandar email de notificacion
        return True
            
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
        was_following = self._del_follows(following)
        if was_following:
            counter_result = self.counters(async=True) # obtiene los contadores de self
            follow_query = UserCounter.all().ancestor(following) # obtiene los contadores del otro usuario
            follow_result = follow_query.run()
            counter_result = counter_result.next()  # sumamos uno al contador de following
            follow_result = follow_result.next()  # sumamos uno al contador de followers del otro usuario
            counter_result.set_followings(-1)
            follow_result.set_followers(-1)
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
        last_follow = followiterator.next()  # como estan ordenados por fecha de creacion, carga el primero que seria el ultimo indice.
        if len(last_follow.following) < TIMELINE_PAGE_SIZE*2:  # un maximo de usuarios en este index para que las listas no sean lentas
            last_follow.following.append(key)
        else:  # creamos un index nuevo
            last_follow = UserFollowingIndex(parent=self, following=[key])
        timeline = UserTimelineSystem(user = key, instance = self, msg_id=100)
        put = db.put_async([last_follow, timeline])
        put.get_result()
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
            index.put()
            return True
        return False
        
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
        
from helpers import UserHelper
from models_acc import *