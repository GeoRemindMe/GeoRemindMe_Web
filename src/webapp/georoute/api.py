# coding:utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the Affero General Public License (AGPL) as published 
by Affero, as published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

You should have received a copy of the GNU Affero General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""

"""
.. module:: api
    :platform: appengine
    :synopsis: public API for Georoute
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""
from google.appengine.ext import db

from geouser.models import User
from models import RouteUserPoint, RouteUserPath, RoutePath, RoutePoint
from exceptions import *
from utils import *

MIN_PATH_LENGTH = 3 #the minimal number of points needed to create a new path
"""Minimun number of points needed to add or search a path

    value: 5
"""

def add_point(user, point):
    """Add a new RouteUserPoint for the user.
    If the user already has this point, returns it

    :param user: The user adding the point
    :type user: User
    :type user: :class:`georemindme.models.User`
    :param point: The point you want to add
    :type point: :class:`db.GeoPt`
    :returns:  RouteUserPoint -- The RouteUserPoint added
    :raises: :class:`AttributeError`
    """
    if not isinstance(user, User):
        raise AttributeError('user must be %s' % str(User))
    if not isinstance(point, db.GeoPt):
        raise AttributeError('point must be %s' % str(db.GeoPt))
    
    return RouteUserPoint.objects.get_or_insert(user, point)

def add_path(user, points):
    """Add a new path for the user
    The order of the points is important, two paths with the same points but with different order, are different paths

    :param user: The user adding the path
    :type user: :class:`georemindme.models.User`
    :param points: List of points, min. length: :py:const:`MIN_PATH_LENGTH`
    :type points: :class:`db.GeoPt`
    :returns: RouteUserPath -- The RouteUserPath added
    :raises: :class:`NoPoints`, :class:`AttributeError`
    """
    if not isinstance(user, User):
        raise AttributeError('user must be %s' % str(User))
    if len(points) < MIN_PATH_LENGTH:
        raise NoPoints('Needed %s or more points' % MIN_PATH_LENGTH)
      
    return RouteUserPath.objects.get_or_insert(user, points)

def search_path(user=None, points=None, sort=True, aprox=True):
    """Search all the possible paths for the user and points
    Search paths from this user and all the others system's paths
    If user is None, search all the paths for those points
    
    :param user: The user looking for his path
    :type user: :class:`georemindme.models.User`
    :param points: List of points, min. length: :py:const:`MIN_PATH_LENGTH`
    :type points: :class:`db.GeoPt`
    :param sort: If you want to get the paths sorted in a list or a dictionary
    :type sort: boolean
    :param aprox: If you want some points to be added
    :type aprox: boolean
    :returns: list of tuples (path_key, occurrences) ordered by the most probable paths
    :returns: dictionary {path_key: occurrences}
    :raises: :class:`NoPoints`, :class:`AttributeError`
    
    >>> [('agtnZW9yZW1pbmRtZXIhCxIJUm91dGVQYXRoIhJycGFvc2VqQXdpekVmRT9fWD8M', 5), ('agtnZW9yZW1pbmRtZXIeCxIJUm91dGVQYXRoIg9ycGF3eWVqQXdpekVvSz8M', 3)]
    """
    
    if user is not None and not isinstance(user, User):
        raise AttributeError('user must be %s' % str(User))
    if points is None or len(points) < MIN_PATH_LENGTH:
        raise NoPoints('Needed %s or more points' % MIN_PATH_LENGTH)
    if aprox:
        points.extend(complete_path(points))
    points = set(points)#remove repeated points
    paths = {}
    if user is not None:
        points = RouteUserPoint.objects.get(user, points)
        paths = RouteUserPath.objects.get_possible_paths(user, points)
        
        points = [p.point for p in points if p is not None]#RoutePath needs RoutePoint not RouteUserPoint
    else:
        points = RoutePoint.objects.get(points)
    paths = RoutePath.objects.get_possible_paths(points=points, possiblePaths=paths)
    if sort:
        return sort_path_dict(paths)
    return paths

def search_path_user(user, points, sort=True, aprox=True):
    """Search all the possible paths from this user and points
    Only returns the paths the user has added or done
    
    :param user: The user looking for his path
    :type user: :class:`georemindme.models.User`
    :param points: List of points, min. length: :py:const:`MIN_PATH_LENGTH`
    :type points: :class:`db.GeoPt`
    :param aprox: If you want some points to be added
    :type aprox: boolean
    :returns: list of tuples (path_key, occurrences) ordered by the most probable paths
    :raises: :class:`NoPoints`, :class:`AttributeError`
    
    >>> [('agtnZW9yZW1pbmRtZXIhCxIJUm91dGVQYXRoIhJycGFvc2VqQXdpekVmRT9fWD8M', 5), ('agtnZW9yZW1pbmRtZXIeCxIJUm91dGVQYXRoIg9ycGF3eWVqQXdpekVvSz8M', 3)]
    """
    if not isinstance(user, User):
        raise AttributeError('user must be %s' % str(User))
    if len(points) < MIN_PATH_LENGTH:
        raise NoPoints('Needed %s or more points' % MIN_PATH_LENGTH)
    if aprox:
        points.extend(complete_path(points))
    points = set(points)#remove repeated points
    points = RouteUserPoint.objects.get(user, points)
    paths = RouteUserPath.objects.get_possible_paths(user, points)
    if sort:
        return sort_path_dict(paths)
    return paths

def get_path(path):
    """Get the path
    
    :param path: The path's key
    :type path: :class:`db.Key` or string
    :returns: :class:`georoute.models.RoutePath` or None
    :raises: :class:`KindError`
    """
    return RoutePath.get(path)
    
    
