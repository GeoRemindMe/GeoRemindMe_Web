from google.appengine.ext import db

from georemindme.models_indexes import Invitation
    
class SuggestionFollowersIndex(db.Model):
    keys = db.ListProperty(db.Key)
    count = db.IntegerProperty(default = 0)
    
class SuggestionCounter(db.Model):
    """Contadores para evitar usar count().
        Podriamos actualizarlos en tiempo real o con algun proceso de background?
    """ 
    followers = db.IntegerProperty(default=0)
    comments = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    
    def _change_counter(self, prop, value):
        obj = UserCounter.get(self.key())
        oldValue = getattr(obj, prop) #  obtiene el valor actual
        value = oldValue+value
        if value < 0:
            raise ValueError
        setattr(obj, prop, value)
        db.put_async(obj)
        return value
         
    def set_followers(self, value=1):
        return db.run_in_transaction(self._change_counter, 'followers', value)
    
    def set_comments(self, value=1):
        return db.run_in_transaction(self._change_counter, 'comments', value)