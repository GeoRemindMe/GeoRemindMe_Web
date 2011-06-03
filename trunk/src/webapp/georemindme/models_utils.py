from google.appengine.ext import db

class Counter(db.Model):
    counter = db.IntegerProperty()
    model = db.StringProperty()
    def _increment_counter(self, key):
        obj = Counter.get(key)
        obj.counter += 1
        obj.put()
        return obj.counter
    
    @classmethod
    def get_counter(cls, model):
        '''
        return the new counter incremented
        '''
        counter = Counter.all(keys_only=True).filter('model =', model).get()#load only the counter key, for the model
        if not counter:#new model, create a new counter
            counter = Counter(counter=1, model=model)
            counter.put()
            counter = counter.key()
        return db.run_in_transaction(cls._increment_counter, Counter(), counter)
