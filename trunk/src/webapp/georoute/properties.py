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

PRECISION = 3 #the decimal precision of the RoutePoint position

class RoutePointProperty(db.GeoPtProperty):
    '''
    Save the point with 3 decimal
    Work like a original db.GeoPtProperty
    '''
    def get_value_for_datastore(self, model_instance):
        raw = super(self.__class__, self).get_value_for_datastore(model_instance)

        raw.lat = round(raw.lat, PRECISION)
        raw.lon = round(raw.lon, PRECISION)
        
        return raw
    
    def make_value_from_datastore(self, value):
        return super(self.__class__, self).make_value_from_datastore(value)
        
        
        
        