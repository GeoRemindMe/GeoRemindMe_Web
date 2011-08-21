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

from georemindme.models import User

class RoutePathIndex(db.Model):
    '''
    Saves the list of points from a path
    '''
    points = db.ListProperty(db.Key)
    
class RouteUserPathIndex(db.Model):
    user = db.ReferenceProperty(User)
    points = db.ListProperty(db.Key)