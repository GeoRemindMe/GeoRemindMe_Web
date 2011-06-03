# coding:utf-8
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
"""
.. module:: exceptions
    :platform: appengine
    :synopsis: exceptions for GeoRoute
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""

class NoChanges(Exception):
    value = "This instance can't be changed"
    
class NoPoints(Exception):
    value = "More points needed to be able to find a path"
    