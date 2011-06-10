from google.appengine.ext import db


class Counter(db.Model):
    counter = db.IntegerProperty()
    model = db.StringProperty()
    
    @classmethod
    def get_counter(cls, model):
        '''
        return the new counter incremented
        '''
        def _increment_counter(key):
            obj = Counter.get(key)
            obj.counter += 1
            obj.put()
            return obj.counter
        
        counter = Counter.all(keys_only=True).filter('model =', model).get()  # load only the counter key, for the model
        if not counter:  # new model, create a new counter
            counter = Counter(counter=0, model=model)
            counter.put()
            counter = counter.key()
        return db.run_in_transaction(_increment_counter, counter)
    
class Visibility(db.Model):
    """Metodos comunes heredados por todas las Clases que necesiten visibilidad"""
    _vis = db.StringProperty(required = True, choices = ['public', 'private', 'shared',], default = 'public')
    
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

#  from http://blog.notdot.net/2010/04/Pre--and-post--put-hooks-for-Datastore-models

class HookedModel(db.Model):
    def _pre_put(self):
        pass
    
    def put(self, *kwargs):
        self._pre_put()
        super(HookedModel, self).put(*kwargs)
        self._post_put()
        
    def _post_put(self):
        pass

old_put = db.put
def hooked_put(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, HookedModel):
            model._pre_put()
    old_put(models, **kwargs)
    for model in models:
        if isinstance(model, HookedModel):
            model._post_put()
db.put = hooked_put