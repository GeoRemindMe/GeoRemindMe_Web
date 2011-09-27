# coding=utf-8

"""
.. module:: properties
    :platform: appengine
    :synopsis: Propiedades propias para el datastore
"""

from google.appengine.ext import db
from django.utils.translation import gettext_lazy as _


class PasswordProperty(db.TextProperty):
    """
        Extends default TextProperty, so we are sure that passwords are always saved encrypted with SHA1
    """
    def get_value_for_datastore(self, model_instance):
        """
        Extract the value from a model instance and convert it to a encrypted password that goes in the datastore. 
        """
        raw = super(self.__class__, self).get_value_for_datastore(model_instance)
        return str(raw)
#        return raw
#        if raw is None:
#            raise ValueError(_("Password can't be empty"))
#        try:
#            if len(raw) > 12:
#                alg, seed, passw = raw.split('$')
#                return raw# the password is encrypted
#        except Exception:
#            pass
#        
#        if len(raw) < 5 or len(raw) > 12:
#            raise ValueError(_("Invalid password"))
#        if re.search(r'[^a-zA-Z0-9]', raw):
#            raise ValueError(_("Invalid password"))
#        
#        from random import random
#        alg = "sha1"
#        seed = sha_constructor(str(random()) + str(random())).hexdigest()[:5]
#        passw = sha_constructor(seed + raw).hexdigest()
#        
#        return '%s$%s$%s' % (alg, seed, passw)

    def make_value_from_datastore(self, value):
        """
        Convert a value as found in the datastore to string. 
        """
        if value is None:
            return None
        
        return unicode(value)
    
    def validate(self, value):
        value = str(value)
        try:
            alg, seed, passw = value.split('$')
            return value            
        except:# no esta codificado el password, lo codificamos
            import re
            if len(value) < 5 or len(value) > 12:
                raise ValueError(_("Invalid password"))
            if re.search(u'[^a-zA-Z0-9]', value):
                raise ValueError(_("Invalid password"))
            from random import random
            from django.utils.hashcompat import sha_constructor
            alg = "sha1"
            seed = sha_constructor(str(random()) + str(random())).hexdigest()[:5]
            passw = sha_constructor(seed + str(value)).hexdigest()
            return '%s$%s$%s' % (alg, seed, passw)


class UsernameProperty(db.StringProperty):
    '''
        Amplia la clase string para controlar que no se usen caracteres no permitidos
    '''
    def get_value_for_datastore(self, model_instance):
        raw = super(self.__class__, self).get_value_for_datastore(model_instance)
        
        if raw is None:
            return None
        raw = raw.lower()
        if raw == 'none':
            raise ValueError(_("Invalid username"))
        if len(raw) < 5:
            raise ValueError(_("Invalid username"))
        import re
        if re.search(r'[^a-z0-9_]', raw):
            raise ValueError(_("Invalid username"))
        return str(raw)
    

class JSONProperty(db.Property):
    from google.appengine.api import datastore_types
    def get_value_for_datastore(self, model_instance):
        value = super(JSONProperty, self).get_value_for_datastore(model_instance)
        return self._deflate(value)
    
    def validate(self, value):
        return self._inflate(value)
    
    def make_value_from_datastore(self, value):
        return self._inflate(value)
    
    def _inflate(self, value):
        if value is None:
            return {}
        if isinstance(value, unicode) or isinstance(value, str):
            from django.utils import simplejson
            return simplejson.loads(value)
        return value
    
    def _deflate(self, value):
        from django.utils import simplejson
        return simplejson.dumps(value)
    data_type = datastore_types.Text
        
        
        
        
