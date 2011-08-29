# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.


"""
class ModelWrapper(object):
    model = None
    header_list = []
    
    def __init__(self, *args, **kwargs):
        self.model = kwargs['model']
        self.header_list = kwargs['header_list']
        
    def list(self, offset=0, limit=500):
        '''
        return a dict with all the values in header_list
        '''
        query = self._load().fetch(limit=limit, offset=offset)
        lists = {}
        for m in query:
            lists[str(m.key())] = {}
            try:
                if len(self.header_list) == 0:
                    for k,v in m.__dict__.iteritems():
                        lists[str(m.key())][k] = v
                for h in self.header_list:
                    lists[str(m.key())][h] = m.__dict__['_%s' % h]
            except:
                pass
                
        return lists
    
    def get(self, *args, **kwargs):
        if 'key' in kwargs:
            from google.appengine.ext.db import Key
            return self.model.get(Key(encoded=kwargs['key']))
        if all(['attr' in kwargs, 'value' in kwargs]):
            return self._load().filter('%s =' % kwargs['attr'], kwargs['value']).get()
        
        raise TypeError()
        
    def _load(self):
        return self.model.all()
        
        
class AdminModel(object):
    '''
        This class will have the information needed to admin a model.
        Create a new class for all the models you want and register it.
        
        Properties:
            model : the model you need to admin.
            header_list : the fields you want to see in list view.
            form : the AdminForm
            description : A little description of the model
    '''
    model = None
    header_list = []
    form = None
    description = 'Add description here'
    
    def __init__(self):
        self.wrapper = ModelWrapper(model=self.model, header_list=self.header_list)
        
    def list(self, offset=0, limit=500):
        return self.wrapper.list(offset, limit)
    
    def get(self, *args, **kwargs):
        return self.wrapper.get(*args, **kwargs)
       
from django import forms
class AdminForm(forms.Form):
    pass
            
_models = {}

def register(*args):
    '''
        Register the models to the admin panel
    '''
    for model in args:
        instance = model()
        _models[str(instance.model.__name__)] = instance
        
        
def getAdminModel(name):
    '''
        Get the registered admin instance for a model registered
        getAdminModel('User')
    ''' 
    try:
        return _models[name]
    except:
        raise Exception('%s does not exists' % str(name))
    
        