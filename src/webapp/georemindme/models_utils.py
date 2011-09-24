# coding=utf-8

"""
.. module:: models_utils
    :platform: appengine
    :synopsis: Modelos comunes a todo el proyecto
"""


from google.appengine.ext import db
from django.utils.translation import gettext_lazy as _


class _Do_later_ft(db.Model):
    instance_key = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    last_try = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def try_again(cls):
        """
            Reintenta añadir a fusion tables los objetos 
            que fallaron, deben implementar el metodo insert_ft()
        """
        queries = cls.all()
        for q in queries:
            try:
                instance = db.get(q.instance_key)
                instance.insert_ft()
                q.delete()
            except:
                q.put()


SHARDS = 5
class ShardedCounter(db.Model):
    """
        Contador sharded
        instance es el key del objeto al que apunta
    """
    instance_key = db.ReferenceProperty(None)
    instance = db.TextProperty()
    count = db.IntegerProperty(required=True, default=0)
    
    @classmethod
    def get_count(cls, instance):
        '''
            Returns the value of the counter, is counters is not in memcache, 
            counts all the sharded counters
        ''' 
        from google.appengine.api import memcache
        total = memcache.get(str(instance))
        if total is None:
            total = 0
            counters = cls.all().filter('instance_key =', instance)
            for counter in counters:
                total += counter.count
            memcache.add(str(instance), str(total), 60)
        return int(total)
    
    @classmethod
    def increase_counter(cls, instance, count):
        '''
            Increment the counter of given key
        '''
        from google.appengine.api import memcache
        def increase():
            import random
            index = random.randint(0, SHARDS-1)#select a random shard to increases
            shard_key = str(instance) + str(index)#creates key_name
            counter = cls.get_by_key_name(shard_key)
            if not counter:#if counter doesn't exist, create a new one
                counter = cls(key_name=shard_key, instance_key=instance)
            counter.count += count
            counter.put()
        
        db.run_in_transaction(increase)
        if count > 0:
            memcache.incr(str(instance), initial_value=0)
        else:
            memcache.decr(str(instance), initial_value=0)
    

VISIBILITY_CHOICES = (
          ('public', _('Public')),
          ('private', _('Private')),
          ('shared', _('Shared')),
                      )
class Visibility(db.Model):
    """Metodos comunes heredados por todas las Clases que necesiten visibilidad"""
    _vis = db.StringProperty(required = True, choices = ('public', 'private', 'shared'), default = 'public')
    
    def _get_visibility(self):
        return self._vis
    
    def _is_public(self):
        if self._vis == 'public':
            return True
        return False
    
    def _is_private(self):
        if self._vis == 'private':
            return True
        return False
    
    def _is_shared(self):
        if self._vis == 'shared':
            return True
        return False
    
    def user_invited(self, user, set_status=None):
        '''
        Comprueba que un usuario ha sido invitado a la lista
            
            :param user: Usuario que debe estar invitado
            :type user: :class:`geouser.models.User`
            :param set_status: Nuevo estado para la invitacion
            :type set_status: :class:`integer`
            
            :returns: True si esta invitado, False en caso contrario
        '''
        from georemindme.models_indexes import Invitation
        if hasattr(self, 'instance'):
            obj = self.instance
        else:
            obj = self
        if set_status is None:
            invitation = Invitation.objects.is_user_invited(obj, user)
            return invitation
        else:
            invitation = Invitation.objects.get_invitation(obj, user)
            if invitation is not None:
                invitation.set_status(set_status)
        return invitation
    
    def send_invitation(self, sender, to):
        if not self.is_saved():
            raise NotImplementedError
        if sender.key() == self.user.key():
            if hasattr(self, 'instance'):
                obj = self.instance
            else:
                obj = self
            if obj._is_private():
                obj._vis = 'shared'
            from georemindme.models_indexes import Invitation
            invitation = Invitation.send_invitation(sender=sender, to=to, instance=obj)
            if invitation is not None:
                return True
            return False
        else:
            from exceptions import ForbiddenAccess
            raise ForbiddenAccess


#  from http://blog.notdot.net/2010/04/Pre--and-post--put-hooks-for-Datastore-models
class HookedModel(db.Model):
    def _pre_put(self):
        pass
    
    def put(self, **kwargs):
        self.put_async().get_result()
        return self._post_put_sync(**kwargs)
        
    def _post_put(self):
        pass
    
    def _post_put_sync(self, **kwargs):
        pass
    
    def _pre_delete(self):
        pass
    
    def delete(self):
        return self.delete_async().get_result()
    
    def _post_delete(self):
        pass
    
    def put_async(self,**kwargs):
        return db.put_async(self)
    
    def delete_async(self):
        return db.delete_async(self)


old_async_put = db.put_async
def hokked_put_async(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, HookedModel):
            model._pre_put()
    async = old_async_put(models, **kwargs)
    get_result = async.get_result
    def get_result_with_callback():
        for model in models:
            if isinstance(model, HookedModel):
                model._post_put()
        return get_result()
    async.get_result = get_result_with_callback
    return async
db.put_async = hokked_put_async


old_async_delete = db.delete_async
def hokked_delete_async(models):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, HookedModel):
            model._pre_delete()
    async = old_async_delete(models)
    get_result = async.get_result
    def get_result_with_callback():
        for model in models:
            if isinstance(model, HookedModel):
                model._post_delete()
        return get_result()
    async.get_result = get_result_with_callback
    return async
db.delete_async = hokked_delete_async


old_put = db.put
def hokked_put(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, HookedModel):
            model._pre_put()
        old_put(models, **kwargs)
        if isinstance(model, HookedModel):
            model._post_put_sync(**kwargs)
db.put = hokked_put


old_delete = db.delete
def hokked_delete(models):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, HookedModel):
            model._pre_delete()
        model.delete()
        if isinstance(model, HookedModel):
            model._post_delete()
db.delete = hokked_delete