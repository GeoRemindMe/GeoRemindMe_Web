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
import re
from google.appengine.ext import db

from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext as _


class PasswordProperty(db.TextProperty):
    """
        Extends default TextProperty, so we are sure that passwords are always saved encrypted with SHA1
    """
    def get_value_for_datastore(self, model_instance):
        """
        Extract the value from a model instance and convert it to a encrypted password that goes in the datastore. 
        """
        raw = super(self.__class__, self).get_value_for_datastore(model_instance)
        
        if raw is None:
            raise ValueError(_("Password can't be empty"))
        try:
            if len(raw) > 12:
                alg, seed, passw = raw.split('$')
                return raw# the password is encrypted
        except Exception:
            pass
        
        if len(raw) < 5:
            raise ValueError(_("Invalid password"))
        if re.search(r'[^a-zA-Z0-9]', raw):
            raise ValueError(_("Invalid password"))
        
        from random import random
        alg = "sha1"
        seed = sha_constructor(str(random()) + str(random())).hexdigest()[:5]
        passw = sha_constructor(seed + raw).hexdigest()
        
        return '%s$%s$%s' % (alg, seed, passw)

    def make_value_from_datastore(self, value):
        """
        Convert a value as found in the datastore to string. 
        """
        if value is None:
            return None
        
        return str(value)
    
class UsernameProperty(db.StringProperty):
    '''
        Amplia la clase string para controlar que no se usen caracteres no permitidos
    '''
    def get_value_for_datastore(self, model_instance):
        raw = super(self.__class__, self).get_value_for_datastore(model_instance)
        
        if raw is None:
            return None
        raw = raw.lower()
        if len(raw) < 5:
            raise ValueError(_("Invalid username"))
        if re.search(r'[^a-z0-9]', raw):
            raise ValueError(_("Invalid username"))
        return str(raw)
        
        
        
        
