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
    
    def put(self, **kwargs):
        self.put_async().get_result()
        return self._post_put_sync()
        
    def _post_put(self):
        pass
    
    def _post_put_sync(self):
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