# coding=utf-8

from google.appengine.ext import db, search

from georemindme.decorators import classproperty
from georemindme.paging import *
from georemindme.models_utils import Visibility
from geoalert.models import *
from geolist.models import *

class CommentHelper(object):
    
    def get_by_key(self, key):
        '''
        Obtiene el evento con ese key
        '''
        return Comment.get(key)
    
    def get_by_user(self, user, query_id = None, page=1):
        '''
        Obtiene una lista con todos los comentarios hechos por un usuario
        
            :param user: usuario a buscar
            :type user: :class:`geouser.models.User`
            :param query_id: identificador de la busqueda paginada
            :type query_id: :class:`long`
            :param page: pagina a buscar
            :type page: :class:`integer`
            
            :returns: [query_id, [:class:`geovote.models.Comment`]]
        '''
        q = Comment.all().filter('user =', user)
        p = PagedQuery(q, id = query_id, page_size=15)
        return [p.id, p.fetch_page(page)]
    
    def get_by_instance(self, instance, query_id=None, page=1):
        '''
        Obtiene una lista con todos los comentarios hechos en una instancia
        
            :param instance: objeto al que buscar los comentarios
            :type instance: :class:`db.Model`
            :param query_id: identificador de la busqueda paginada
            :type query_id: :class:`long`
            :param page: pagina a buscar
            :type page: :class:`integer`
            
            :returns: [query_id, [:class:`geovote.models.Comment`]]
        '''
        q = Comment.all().filter('instance =', instance)
        p = PagedQuery(q, id = query_id, page_size=15)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id_user(self, id, user):
        comment = Comment.get_by_id(int(id))
        if comment.user.key() == user.key():
            return comment
        if comment._is_public():
            if comment.instance.user.key() == user.key():
                return comment
            elif comment.instance._is_public():
                return comment
            elif comment.instance._is_shared() and comment.instance.user_invited(user):
                return comment
        return None        
        
    
class Comment(Visibility):
    '''
    Se puede comentar cualquier objeto del modelo
    '''
    user = db.ReferenceProperty(User, collection_name='comments')
    instance = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now = True)
    msg = db.TextProperty(required=True)
    
    objects = CommentHelper()
    """
    @classproperty
    def objects(self):
        return CommentHelper()
    """
    @property
    def id(self):
        return self.key().id()
    
    @classmethod
    def do_comment(cls, user, instance, msg):
        
        if msg is None or msg == '':
            raise TypeError('msg is empty')
        comment = Comment(user, instance, msg)
        comment.put()
        if getattr(instance, 'counter', None) is not None:
            instance.counter.set_comments()
        return comment
        
    
SHARDS = 5
class VoteCounter(db.Model):
    '''
        Contador sharded
        instance es el key del objeto al que apunta
    '''
    instance = db.TextProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)
    
    @classmethod
    def get_count(cls, instance):
        '''
            Returns the value of the counter, is counters is not in memcache, 
            counts all the sharded counters
        ''' 
        from google.appengine.api import memcache
        instance=str(instance)
        total = memcache.get(instance)
        if not total:
            total = 0
            counters = VoteCounter.gql('WHERE instance = :1', instance)
            for counter in counters:
                total += counter.count
            memcache.add(instance, str(total), 60)
        return int(total)
    
    @classmethod
    def increase_counter(cls, instance, count):
        '''
            Increment the counter of given key
        '''
        from google.appengine.api import memcache
        instance=str(instance)
        def increase():
            import random
            index = random.randint(0, SHARDS-1)#select a random shard to increases
            shard_key = instance + str(index)#creates key_name
            counter = VoteCounter.get_by_key_name(shard_key)
            if not counter:#if counter doesn't exist, create a new one
                counter = VoteCounter(key_name=shard_key, instance=instance)
            counter.count += count
            counter.put()
        db.run_in_transaction(increase)
        if count > 0:
            memcache.incr(instance, initial_value=0)
        else:
            memcache.decr(instance, initial_value=0)


class VoteHelper(object):
    def user_has_voted(self, user, instance_key):
        '''
        Comprueba que un usuario ya ha realizado un voto
        
            :param user: usuario que realiza el voto
            :type user: :class:`geouser.models.User`
            :param instance_key: key del objeto al que se vota
            :type instance_key: :class:`string`
            
            :returns: True si ya ha votado, False en caso contrario
        '''
        vote = db.GqlQuery('SELECT __key__ FROM Vote WHERE instance = :ins AND user = :user', ins=instance_key, user=user.key()).get()
        if vote is not None:
            return True
        return False
    
    def get_user_vote(self, user, instance_key):
        '''
        Obtiene el voto de un usuario a un objeto determinado
        
            :param user: usuario a buscar
            :type user: :class:`geouser.models.User`
            :param instance_key: clave del objeto al que hay que buscar el voto
            :type instance_key: :class:`db.Key`
            
            :returns: :class:`geovote.models.Vote` o None
        '''
        vote = Vote.all().filter('instance =', instance_key).filter('user =', user).get()
        return vote
    
    def get_vote_counter(self, instance_key):
        '''
        Obtiene el contador de votos de objeto determinado
        
            :param instance_key: clave del objeto al que hay que buscar el voto
            :type instance_key: :class:`db.Key`
            
            :returns: :class:`integer`
        '''
        return VoteCounter.get_count(instance_key)
        
    

class Vote(db.Model):
    
    user = db.ReferenceProperty(User, collection_name='votes')
    instance = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty(default=0)
    
    objects = VoteHelper()
    
    @classmethod
    def do_vote(cls, user, instance, count=1):
        '''
        Añade un voto de un usuario a una instancia
        
            :param user: usuario que realiza la votacion
            :type user: :class:`geouser.models.User`
            :param instance: objeto al que se vota
            :type instance: :class:`object`
            :param count: valoracion del voto
            :type count: :class:`integer`
            
            :returns: True si se realizo el voto, False si ya se habia votado
        '''
        count = int(count)
        vote = cls.objects.get_user_vote(user, instance.key())
        if vote is not None:
            if count < 0:
                VoteCounter.increase_counter(vote.instance.key(), -1)
                vote.delete()
                return True
            return False
        vote = Vote(user=user, instance=instance, count=1)
        vote.put()
        return True
    
    def put(self):
        if not self.is_saved():
            contador = VoteCounter.increase_counter(self.instance.key(), self.count)
        super(Vote, self).put()
        
    
