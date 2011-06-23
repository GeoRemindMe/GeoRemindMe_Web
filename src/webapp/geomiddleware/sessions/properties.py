import pickle
import copy

from google.appengine.ext import db


# https://github.com/Arachnid/aetycoon/blob/master/__init__.py
class PickleProperty(db.Property):
    '''
    A property for storing complex objects in the datastore in pickled form.
    
        Example usage:
        
        >>> class PickleModel(db.Model):
        ... data = PickleProperty()
        
        >>> model = PickleModel()
        >>> model.data = {"foo": "bar"}
        >>> model.data
        {'foo': 'bar'}
        >>> model.put() # doctest: +ELLIPSIS
        datastore_types.Key.from_path(u'PickleModel', ...)
        
        >>> model2 = PickleModel.all().get()
        >>> model2.data
        {'foo': 'bar'}
    '''
    
    def default_value(self):
        """
        If possible, copy the value passed in the default= keyword argument.
        This prevents mutable objects such as dictionaries from being shared across
        instances.
        """
        return copy.copy(self.default)

    def get_value_for_datastore(self, model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        if value is not None:
            return db.Blob(pickle.dumps(value))

    def make_value_from_datastore(self, value):
        if value is not None:
            return pickle.loads(str(value))
