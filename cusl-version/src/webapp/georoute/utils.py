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
.. module:: utils
    :platform: appengine
    :synopsis: Some useful functions
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""
from math import fabs
from google.appengine.ext.db import GeoPt
from itertools import tee, izip

def sort_path_dict(dict, reverse=True):
    """Sorts a list from a dict by value,
        .. code::
                
                Dictionary:
                    {
                        PathKey : count,
                        ...
                    }
                dict.iteritems() returns a tuple (key, value)
                itemgetter(1), return the value
    """
    from operator import itemgetter 
    return sorted(dict.iteritems(), key=itemgetter(1), reverse=reverse)

def _dichotomy(points, list=[]):
    '''
        Añade puntos en la mitad, similar a una diagonal
    '''
    if len(list) > 25:
        return list
    if points[0] == points[1]:
        return list
    dLat = round((points[0].lat - points[1].lat), 3)/2
    dLon = round((points[0].lon - points[1].lon), 3)/2
    if fabs(dLat) < 0.001 and fabs(dLon) < 0.001:
        return list
    pointN = GeoPt(lat=round(points[0].lat-dLat,3), lon=round(points[0].lon-dLon,3))
    _dichotomy((points[0], pointN), list=list)
    _dichotomy((pointN, points[1]), list=list)
    list.append(pointN)
    return list

def _dichotomy_lat(points, list=[]):
    '''
        Añade puntos en la mitad, pero solo modificando la latitud
    '''
    if len(list) > 25:
        return list
    if points[0] == points[1]:
        return list
    dLat = round((points[0].lat - points[1].lat), 3)/2
    if fabs(dLat) < 0.001:
        return list
    pointN = GeoPt(lat=round(points[0].lat-dLat,3), lon=points[0].lon)
    _dichotomy_lat((points[0], pointN), list=list)
    _dichotomy_lat((pointN, points[1]), list=list)
    list.append(pointN)
    return list

def _dichotomy_lon(points, list=[]):
    '''
        Añade puntos en la mitad, pero solo modificando la longitud
    '''
    if len(list) > 25:
        return list
    if points[0] == points[1]:
        return list
    dLon = round((points[0].lon - points[1].lon), 3)/2
    if fabs(dLon) < 0.001:
        return list
    pointN = GeoPt(lat=points[0].lat, lon=round(points[0].lon-dLon,3))
    _dichotomy_lon((points[0], pointN), list=list)
    _dichotomy_lon((pointN, points[1]), list=list)
    list.append(pointN)
    return list

def complete_path(points):
    """Creates a 'buffer' of new points around the original user points
        
        :param points: list of points
        :type points: :class:`db.GeoPt`
        :returns: list of points
    """
    # TODO: cambiar este fucking code :D
    list = []
    [_dichotomy_lat(p, list=list) for p in pair(points)]
    list2 = []
    [_dichotomy_lon(p, list=list2) for p in pair(points)]
    list.extend(list2)
    list3 = []
    [_dichotomy(p, list=list3) for p in pair(points)]
    list.extend(list3)
    return list

def pair(iterable):
    """Returns a tuple with two consecutives elements from a list
    .. note::
       
        http://docs.python.org/library/itertools.html#recipes
    
    """
    a, n = tee(iterable)#returns 2 iterators from a single iterable
    next(n, None)#move the n iterator to the next value
    return izip(a,n)#returns a tuple with the two elements.
    
    