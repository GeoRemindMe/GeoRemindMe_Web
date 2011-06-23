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

from google.appengine.ext import db

class HookedModel(db.Model):
    '''
        A new model class providing hooks for some checks
    '''
    def _pre_put(self):
        '''
            This method get executes before saving the instance
        '''
        pass
    
    def _populate_internal_entity(self, *args, **kwargs):
        '''
            Called when a instance will be saved in datastore
        '''
        self._pre_put()
        return db.Model._populate_internal_entity(self, *args, **kwargs)