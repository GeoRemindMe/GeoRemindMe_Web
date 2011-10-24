# coding=utf-8

"""
.. module:: models_utils
    :platform: appengine
    :synopsis: Modelos comunes a todo el proyecto
"""


from google.appengine.ext import db
from google.appengine.api import memcache
from django.utils.translation import gettext_lazy as _


class _Do_later_ft(db.Model):
    instance_key = db.ReferenceProperty(None)
    created = db.DateTimeProperty(auto_now_add=True)
    last_try = db.DateTimeProperty(auto_now=True)
    update = db.BooleanProperty(default=False)
    
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
        memclient = memcache.Client()
        total = memclient.get(str(instance))
        if total is None:
            total = 0
            counters = cls.all().filter('instance_key =', instance)
            for counter in counters:
                total += counter.count
            memclient.add(str(instance), str(total), 60)
        return int(total)
    
    @classmethod
    def increase_counter(cls, instance, count):
        '''
            Increment the counter of given key
        '''
        memclient = memcache.Client()
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
            memclient.incr(str(instance), initial_value=0)
        else:
            memclient.decr(str(instance), initial_value=0)
    

VISIBILITY_CHOICES = (
          ('public', _('Publica')),
          ('private', _('Privada')),
          ('shared', _('Compartida')),
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
