# coding=utf-8

"""
.. module:: models
    :platform: appengine
    :synopsis: Modelo de voto y comentario
"""


from django.utils.translation import gettext_lazy as _
from google.appengine.ext import db

from georemindme.models_utils import Visibility
from geouser.models import User


class CommentHelper(object):
    """ Helper de la clase comentario """
    def get_by_id(self, id):
        try:
            id = long(id)
        except:
            return None
        comment = Comment.get_by_id(id)
        if comment is not None:
            if comment.deleted:
                return None
            if comment._is_public():
                return comment
        return None
        
    def get_by_key(self, key):
        """
        Obtiene el evento con ese key
        """
        return Comment.get(key)
    
    def get_by_user(self, user, query_id = None, page=1, querier=None):
        """
        Obtiene una lista con todos los comentarios hechos por un usuario
        
            :param user: usuario a buscar
            :type user: :class:`geouser.models.User`
            :param query_id: identificador de la busqueda paginada
            :type query_id: :class:`long`
            :param page: pagina a buscar
            :type page: :class:`integer`
            
            :returns: [query_id, [:class:`geovote.models.Comment`]]
        """
        if querier is not None and not isinstance(querier, User):
            raise TypeError
        from georemindme.paging import PagedQuery
        from google.appengine.api import datastore
        q = datastore.Query('Comment')
        q.update({'user =': user.key(), 'deleted =': False})
        q.Order('-created')
        # q = Comment.all().filter('user =', user).filter('deleted =', False).order('-created')
        p = PagedQuery(q, id = query_id, page_size=7)
        comments = p.fetch_page(page)
        return [p.id,  [{'id': comment.id,
                        'created': comment.created,
                        'modified': comment.modified, 
                        'msg': comment.msg,
                        'username': comment.user.username,
                        'instance': comment.instance if comment.instance is not None else None,
                        'has_voted':  Vote.objects.user_has_voted(querier, comment.key()) if querier is not None else None,
                        'vote_counter': comment.votes,
                        }
                       for comment in comments]]
    
    def get_by_instance(self, instance, query_id=None, page=1, querier = None, async=False):
        """
        Obtiene una lista con todos los comentarios hechos en una instancia
        
            :param instance: objeto al que buscar los comentarios
            :type instance: :class:`db.Model`
            :param query_id: identificador de la busqueda paginada
            :type query_id: :class:`long`
            :param page: pagina a buscar
            :type page: :class:`integer`
            
            :returns: [query_id, [:class:`geovote.models.Comment`]]
        """
        if querier is not None and not isinstance(querier, User):
            raise TypeError
        from georemindme.paging import PagedQuery
        from google.appengine.api import datastore

        q = Comment.all().filter('instance =', instance).filter('deleted =', False).order('-created')
        p = PagedQuery(q, id = query_id, page_size=7)
        if async:
            return p.id, q.run()
        comments = p.fetch_page(page)
        return [p.id, [{'id': comment.id,
                        'created': comment.created,
                        'modified': comment.modified, 
                        'msg': comment.msg,
                        'username': comment.user.username,
                        'instance': comment.instance if comment.instance is not None else None,
                        'has_voted':  Vote.objects.user_has_voted(querier, comment.key()) if querier is not None else None,
                        'vote_counter': comment.votes,
                        }
                       for comment in comments]]
        
    def load_comments_from_async(self, query_id, comments_async, querier):
        if querier is not None and not isinstance(querier, User):
            raise TypeError
        comments_loaded = []
        for comment in comments_async:
            comments_loaded.append({'id': comment.id,
                                    'created': comment.created,
                                    'modified': comment.modified, 
                                    'msg': comment.msg,
                                    'username': comment.user.username,
                                    'instance': comment.instance if comment.instance is not None else None,
                                    'has_voted':  Vote.objects.user_has_voted(querier, comment.key()) if querier is not None else None,
                                    'vote_counter': comment.votes,
                                    }
                                  )
            if len(comments_loaded) > 7:
                    break
        return [query_id, comments_loaded]
    
    def get_by_id_user(self, id, user):
        try:
            id = long(id)
        except:
            return None
        if not isinstance(user, User):
            raise AttributeError()
        comment = Comment.get_by_id(int(id))
        if comment is not None:
            if comment.deleted:
                return None
            if comment.user.key() == user.key():
                return comment
        return None      
    
    def get_by_id_querier(self, id, querier):
        try:
            id = long(id)
        except:
            return None
        if not isinstance(querier, User):
            raise AttributeError()
        
        comment = Comment.get_by_id(id)
        if comment is not None:
            if comment.deleted:
                return None
            if comment.user.key() == querier.key():
                return comment
            elif comment._is_public(): # comentario publico
                return comment
            elif comment.instance.user.key() == querier.key(): # comentario en un objeto publico
                return comment
            elif comment.instance._is_public(): # la instancia es publica, sus comentarios son publicos
                return comment
            elif comment.instance._is_shared() and comment.instance.user_invited(querier): # instancia compartida, usuario invitado
                return comment
        return None     
    
    def get_top_voted(self, instance, querier):
        if querier is not None and not isinstance(querier, User):
            raise TypeError
        if instance is not None:
            import memcache
            top = None #memcache.get(memcache.get('%stopcomments_%s' % (memcache.version, instance.key())))
            if top is None:
                top = Comment.all().filter('instance =', instance).filter('votes >', 0).filter('deleted =', False).order('-votes').fetch(3, 0)
                if top is not None:
                    comments = [{'id': comment.id,
                                'created': comment.created,
                                'modified': comment.modified, 
                                'msg': comment.msg,
                                'username': comment.user.username,
                                'instance': comment.instance if comment.instance is not None else None,
                                'has_voted':  Vote.objects.user_has_voted(querier, comment.key()) if querier is not None else None,
                                'vote_counter': comment.votes,
                        }
                       for comment in top]
                    memcache.set('%stopcomments_%s' % (memcache.version, instance.key()), comments, 300)
        return top
        

class Comment(Visibility):
    """ Se puede comentar cualquier objeto del modelo """
    user = db.ReferenceProperty(User, collection_name='comments')
    instance = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now = True)
    msg = db.TextProperty(required=True)
    deleted = db.BooleanProperty(default=False)
    votes = db.IntegerProperty(default=0)
    
    objects = CommentHelper()

    @property
    def id(self):
        return self.key().id()
    
    def set_votes(self, count):
        def _tx(count):
            obj = Comment.get(self.key())
            obj.votes += count
            if obj.votes < 0:
                obj.votes = 0
            obj.put()
            return obj.votes
        return db.run_in_transaction(_tx, count)
    
    @classmethod
    def do_comment(cls, user, instance, msg):
        
        if msg is None or msg == '':
            raise TypeError('msg is empty')
        comment = Comment(user=user, instance=instance, msg=msg)
        comment.put()
        if getattr(instance, 'counter', None) is not None:
            instance.counter.set_comments()
        from signals import comment_new
        comment_new.send(sender=comment)
        return comment
    
    def to_dict(self):
        return {'id': self.id if self.is_saved() else -1,
                'instance': self.instance.id,
                'created': self.created,
                'modified': self.modified,
                'msg': self.msg,
                'user': self.user,
                }
        
    def delete(self, force=False):
        from signals import comment_deleted
        if force:
            comment_deleted.send(self)
            super(Comment, self).deleted()
        else:
            self.deleted = True
            self.put()
            comment_deleted.send(self)
            

from georemindme.models_utils import ShardedCounter
class VoteCounter(ShardedCounter):
    """
        Contador sharded
        instance es el key del objeto al que apunta
    """
    pass


class VoteHelper(object):
    """ Helper de la clase Vote """
    def user_has_voted(self, user, instance_key):
        """
        Comprueba que un usuario ya ha realizado un voto
        
            :param user: usuario que realiza el voto
            :type user: :class:`geouser.models.User`
            :param instance_key: key del objeto al que se vota
            :type instance_key: :class:`string`
            
            :returns: True si ya ha votado, False en caso contrario
        """
        if isinstance(user, db.Key):
            vote = db.GqlQuery('SELECT __key__ FROM Vote WHERE instance = :ins AND user = :user', ins=instance_key, user=user).get()
        else:
            if not user.is_authenticated():
                return False
            vote = db.GqlQuery('SELECT __key__ FROM Vote WHERE instance = :ins AND user = :user', ins=instance_key, user=user.key()).get()
        if vote is not None:
            return True
        return False
    
    def get_user_vote(self, user, instance_key):
        """
        Obtiene el voto de un usuario a un objeto determinado
        
            :param user: usuario a buscar
            :type user: :class:`geouser.models.User`
            :param instance_key: clave del objeto al que hay que buscar el voto
            :type instance_key: :class:`db.Key`
            
            :returns: :class:`geovote.models.Vote` o None
        """
        vote = Vote.all().filter('instance =', instance_key).filter('user =', user).get()
        return vote
    
    def get_vote_counter(self, instance_key):
        """
        Obtiene el contador de votos de objeto determinado
        
            :param instance_key: clave del objeto al que hay que buscar el voto
            :type instance_key: :class:`db.Key`
            
            :returns: :class:`integer`
        """
        return VoteCounter.get_count(instance_key)
        

class Vote(db.Model):
    """ Se podria votar cualquier objeto """
    user = db.ReferenceProperty(User, collection_name='votes')
    instance = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty(default=0)
    
    objects = VoteHelper()
    
    @property
    def id(self):
        return self.key().id()
    
    @classmethod
    def do_vote(cls, user, instance, count=1):
        """
        Añade un voto de un usuario a una instancia
        
            :param user: usuario que realiza la votacion
            :type user: :class:`geouser.models.User`
            :param instance: objeto al que se vota
            :type instance: :class:`object`
            :param count: valoracion del voto
            :type count: :class:`integer`
            
            :returns: True si se realizo el voto, False si ya se habia votado
        """
        from signals import vote_new, vote_deleted
        count = int(count)
        vote = cls.objects.get_user_vote(user, instance.key())
        if vote is not None:
            if count < 0:
                vote_deleted.send(sender=vote)
                vote.delete()
                return True
            return False
        vote = Vote(user=user, instance=instance, count=1)
        vote.put()
        vote_new.send(sender=vote)
        return True
    
    def to_dict(self):
        return {'id': self.id if self.is_saved() else -1,
                'instance': self.instance.id,
                'created': self.created,
                'user': self.user,
                'count': self.count,
                }
    
    def put(self):
        if not self.is_saved():
            if hasattr(self.instance, 'set_votes'):
                self.instance.set_votes(self.count)
            else:
                contador = VoteCounter.increase_counter(self.instance.key(), self.count)
        super(Vote, self).put()
        
    def delete(self):
        if hasattr(self.instance, 'set_votes'):
                self.instance.set_votes(-1)
        else:
            VoteCounter.increase_counter(self.instance.key(), -1)
        vote_deleted.send(self)
        super(Vote, self).delete()


from watchers import *
