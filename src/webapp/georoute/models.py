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
.. module:: models
    :platform: appengine
    :synopsis: models in the datastore
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""
    # DONE: obtener posibles paths
    # DONE: crear userpath
    # DONE: bug al generar polyline
    # DONE: añadir mas puntos a los paths para las busquedas
    # DONE: crear bigBox
    # TODO: evitar duplicados en routeuserpoint_set de routepoint
    # TODO: dar prioridad a las rutas del usuario
    # TODO: controlar contadores cuando se cargue una ruta
    # TODO: generate_path en transaccion
    # TODO: implementar metodos delete() para borrar tambien las referencias
    # TODO: crear tests
    # TODO: crear documentacion
    # TODO: mirar querys async
    # TODO: cambiar la forma de mirar si es una lista de puntos en los metodos get()

import math
from google.appengine.ext import db
from geouser.models import User

from exceptions import *
from properties import RoutePointProperty, PRECISION
from models_shardcounters import RouteCounter
from models_hookedmodels import HookedModel
from models_indexes import *

class RoutePointHelper(object):
    """Helper function for :class:`RoutePoint`, accesed by :class:`RoutePoint.objects`"""
    def get(self, point, keys_only=False):
        """Returns the :class:`RoutePoint` for this point or list of poitns
        
            :param point: point or list searching
            :type point: :class:`db.GeoPt`
            :param keys_only: True if only wants instances' keys
            :type keys_only: bool
            :returns: None or :class:`RoutePoint`
        """
        if type(point) == type(list()) or type(point) == type(set):
            if keys_only:
                return [db.GqlQuery('SELECT __key__ FROM RoutePoint WHERE point = :1', db.GeoPt(round(p.lat, PRECISION), round(p.lon, PRECISION))).get() for p in point]
            return [RoutePoint.gql('WHERE point = :1', db.GeoPt(round(p.lat, PRECISION), round(p.lon, PRECISION))).get() for p in point]
        return RoutePoint.get_by_key_name('rp%f%f' % (round(point.lat, PRECISION), round(point.lon, PRECISION)))
    
    def get_or_insert(self, point):
        """From a one or list of :class:`db.GeoPt` points, returns or create all the :class:`RoutePoint`
        
            :param point: point searching
            :type point: :class:`db.GeoPt`
            :returns: :class:`RoutePoint` or list of :class:`RoutePoint`
        """
        if type(point) == type(list()):  # if point is a list of points
            listPoints = []
            for p in point:
                tempPoint = self.get(p)
                if tempPoint is None:
                    tempPoint = self.get_or_insert(p)
                listPoints.append(tempPoint)
            return listPoints
        return RoutePoint.get_or_insert(key_name='rp%f%f' % (round(point.lat, PRECISION), round(point.lon, PRECISION)), point=point)
    
class RoutePoint(HookedModel):
    """This Model will save the points for all the paths"""
    point = RoutePointProperty(required=True)
    """The coords of the points, rounded to PRECISION value"""        
    created = db.DateTimeProperty(auto_now_add=True)
    """The date of creation"""
    objects = RoutePointHelper()
        
    @property
    def users(self):
        """The list with all the users who where in this point
        
            :returns: :class:`georemindme.models.User`
        """
        return User.get(([u.user.key() for u in self.routeuserpoint_set]))
    
    @property
    def total(self):
        """The total time this point gets visited"""
        return RouteCounter.get_count(self.key())
    
    def get_routeuserpoint(self, user):
        """Return the :class:`RouteUserPoint` from the user
        
                :param user: the user wanted
                :type user: :class:`georemindme.models.User`
                :returns: :class:`RouteUserPoint`
        """
        return self.routeuserpoint_set.filter('user =', user).get()

    def inc_total(self, value=1):
        """Increases the total times this point gets visited
        
            :param value: value to increases
            :type value: integer
        """
        if value <= 0:
            raise db.BadValueError()
        if value == 1:
            RouteCounter.increase_counter(self.key())
        else:
            for i in xrange(1, value):
                RouteCounter.increase_counter(self.key())

class RoutePathHelper(object):
    """Helper function for :class:`RoutePath`, accesed by :class:`RoutePath.objects`"""
    def get_possible_paths(self, points=None, possiblePaths=None):
        """Get a list of possible paths for the list of points
        
            :param points: list of points
            :type points: :class:`RoutePoint`
            :param possiblePaths: a dictionary (key:value) initialized
            :type possiblePaths: { RoutePath.key() : value }
            :returns: a dict with RoutePath.key():value
        """
        if possiblePaths is None:
            possiblePaths = {}
        for point in points:
            if point is not None:#maybe some points aren't in the database
                indexes = db.GqlQuery("SELECT __key__ FROM RoutePathIndex WHERE points = :1", point.key())
                paths = [k.parent() for k in indexes]
                for path in paths:
                    if str(path) in possiblePaths:
                        possiblePaths[str(path)] += 1
                    else:
                        possiblePaths[str(path)] = 1
        return possiblePaths
    
    def exists_path(self, points=None):
        """Search if this list of points is already a path
            The list order is important, same points in different order, are different paths
            
            :param points: list of points
            :type points: :class:`RoutePoint`
        """
        encodedPoints, encodedLevels = RoutePath()._get_polyline(points)
        return RoutePoint.get_by_key_name('rpa%s' %(encodedPoints))
    
    def get_or_insert(self, points):
        """From list of :class:`db.GeoPt` points, returns or create the :class:`RoutePath`
        
            :param point: point searching
            :type point: :class:`db.GeoPt`
            :returns: :class:`RoutePath`
        """
        path = self.exists_path(points=points)
        if path is None:
            encodedPoints, encodedLevels = RoutePath()._get_polyline(points)
            path = RoutePath.get_or_insert(key_name='rpa%s' % (encodedPoints), encodedPoints=encodedPoints, encodedLevels=encodedLevels)
            pathIndex = RoutePathIndex.get_or_insert(key_name='rpai%s' % (encodedPoints), parent=path, points=[p.key() for p in points])
            path.generate_path()
        return path
            
class RoutePath(HookedModel):
    """Describes all the points doing a path, also saves the total times the path has been correctly predicted"""
    encodedPoints = db.StringProperty()
    """string with the points to pass to google maps"""
    encodedLevels = db.TextProperty()
    """string with the levels encoded""" 
    bigBox = db.TextProperty()
    """box that bounds all the points"""
    created = db.DateTimeProperty(auto_now_add=True)
    """The date of creation"""
    objects = RoutePathHelper()

    def generate_path(self):
        """Generate the path creating all the points"""
        self.bigBox = self._get_bigBox()
        self.put()
        
    @property
    def points(self):
        """Returns a list with all the points in the path"""
        indexes = db.query_descendants(self)
        if indexes.count() == 0:
            raise db.InternalError('Index doesn\'t exist')
        # seria mejor hacer un get() con la lista de cada index en vez de uno agrupando todas las listas
        return RoutePoint.get(reduce(list.__add__,[index.points for index in indexes]))
    
    @property
    def polyline(self):
        """Returns the dict with the points and zoom level to pass to javascript and paint the polyline"""
        
        return {
                'encodedPoints' : self.encodedPoints,
                'encodedLevel' : self.encodedLevels,
                }
        
    @property
    def total(self):
        """The total time this point gets visited"""
        return RouteCounter.get_count(self.key())

    def inc_total(self, value=1):
        """Increases the total times this point gets visited
        
            :param value: value to increases
            :type value: integer
        """
        if value <= 0:
            raise db.BadValueError()
        if value == 1:
            RouteCounter.increase_counter(self.key())
        else:
            for i in xrange(1, value):
                RouteCounter.increase_counter(self.key())
    
    def delete(self):
        indexes = db.query_descendants(self)
        for index in indexes:
            index.delete()
        super(self.__class__, self).delete()
        
    #===========================================================================
    # Encode the points in base32 for google maps API
    # from http://wiki.urban.cens.ucla.edu/index.php/How-to_use_Google_Maps_polyline_encoding_to_compact_data_size
    #===========================================================================
    def _get_polyline(self, points):
        '''
            Generates the polyline string codification
        '''
        i = 0
        plat = 0
        plng = 0
        encodedPoints = ""
        encodedLevels = ""
        
        for i in range(0, len(points)):
            point = points[i]
            level = 3 - i%4                    
            late5 = int(math.floor(point.point.lat * 1e5))
            lnge5 = int(math.floor(point.point.lon * 1e5)) 
            dlat = late5 - plat
            dlng = lnge5 - plng                
            plat = late5
            plng = lnge5                       
        
            encodedPoints += self._encode_signed_number(dlat) + self._encode_signed_number(dlng)
            encodedLevels += self._encode_number(level) 
        return encodedPoints, encodedLevels
    
    def _encode_number(self, value):
        '''
            Encode the point with the base32 format from google
        '''
        encodeString = ""
        while value >= 0x20:
            encodeString += chr((0x20 | (value & 0x1f)) + 63)
            value >>= 5
        encodeString += chr(value + 63)
        return encodeString

    def _encode_signed_number(self, value):
        sgn_num = value << 1
        if value < 0:
            sgn_num = ~(sgn_num)
        return self._encode_number(sgn_num)
    
    def _get_bigBox(self):
        '''
            Generate a big box around all the points
        '''
        points = self.points
        if len(points) != 0:
            points.sort(key=lambda k: k.point.lat)
            upLat = points[0].point.lat
            downLat = points[-1].point.lat
            points.sort(key=lambda k: k.point.lon)
            leftLon = points[0].point.lon
            rightLon = points[-1].point.lon
            
            return u'%s,%s|%s,%s' % (upLat, leftLon, downLat, rightLon)
        return u''

class RouteUserPointHelper(object):
    """Helper function for :class:`RouteUserPoint`, accesed by :class:`RouteUserPoint.objects`"""
    def get(self, user, point):
        """Returns the :class:`RouteUserPoint` for this point or list of points
        
            :param user: The user wanted
            :type user: :class:`georemindme.models.User`
            :param point: point or list searching
            :type point: :class:`db.GeoPt`
            :returns: None or :class:`RouteUserPoint`
        """
        realPoints = RoutePoint.objects.get(point, keys_only=True)
        if type(point) == type(list()) or type(point) == type(set()):
            return [user.routeuserpoint_set.filter('point =', p).get() for p in realPoints]
        return user.routeuserpoint_set.filter('point =', realPoints).get()
        #return RouteUserPoint.get_by_key_name('rup%s%f%f' % (str(user.key()), point.lat, point.lon))
    
    def get_or_insert(self, user, point):
        """From a one or list of :class:`db.GeoPt` points, returns or create all the :class:`RoutePoint`
        
            :param point: point searching
            :type point: :class:`db.GeoPt`
            :returns: :class:`RoutePoint` or list of :class:`RoutePoint`
        """
        if type(point) == type(list()):  # if point is a list of points
            listPoints = []
            for p in point:
                tempPoint = self.get(user, p)
                if tempPoint is None:
                    tempPoint = self.get_or_insert(user, p)
                listPoints.append(tempPoint)
            return listPoints
        rup = self.get(user, point)
        if rup is None:
            rp = RoutePoint.objects.get_or_insert(point)
            rup = RouteUserPoint.get_or_insert(key_name='rup%s%f%f' % (str(user.key()), point.lat, point.lon), parent=rp, user=user, original=point, point=rp)
        return rup        
    
class RouteUserPoint(HookedModel):
    """Saves the relation user-point, the original point the user was, and the total times that user has been there"""
    user = db.ReferenceProperty(User, required=True)
    """owner reference"""
    original = db.GeoPtProperty(required=True)
    """The original coords of the point"""
    point = db.ReferenceProperty(RoutePoint)
    """The coords of the point, rounded to PRECISION value"""
    created = db.DateTimeProperty(auto_now_add=True)
    """The date of creation"""
    objects = RouteUserPointHelper()
    
    def _pre_put(self):
        '''
             The original point can't be changed
        '''
        if self.is_saved():
            if self.original.lat != self._entity['original'].lat or self.original.lon != self._entity['original'].lon or self.point.key() != self._entity['point']:
                raise NoChanges()
        
    @property
    def total(self):
        """The total time this point gets visited"""
        return RouteCounter.get_count(self.key())

    def inc_total(self, value=1):
        """Increases the total times this point gets visited
        
            :param value: value to increases
            :type value: integer
        """
        if value <= 0:
            raise db.BadValueError()
        if value == 1:
            RouteCounter.increase_counter(self.key())
        else:
            for i in xrange(1, value):
                RouteCounter.increase_counter(self.key())

class RouteUserPathHelper(object):
    """Helper function for :class:`RouteUserPath`, accesed by :class:`RouteUserPath.objects`"""
    def get(self, user, path):
        """Returns the :class:`RouteUserPath` for the :class:`RoutePath`
        
            :param user: The user wanted
            :type user: :class:`georemindme.models.User`
            :param path: the path you want his :class:`RouteUserPath`
            :type point: :class:`RoutePath`
            :returns: None or :class:`RouteUserPath`
        """
        return user.routeuserpath_set.filter('path.encodedPoints =', path.encodedPoints).get()
        #return RouteUserPath.get_by_key_name('rupa%s%s' % (str(user.key()), str(path.key())))
    
    def get_possible_paths(self, user, points=None, possiblePaths=None):
        """Get a list of possible paths for the list of points
        
            :param points: list of points
            :type points: :class:`RouteUserPoint`
            :param possiblePaths: a dictionary (key:value) initialized
            :type possiblePaths: { RouteUserPath.key() : value }
            :returns: a dict with RouteUserPath.key():value
        """
        if possiblePaths is None:
            possiblePaths = {}
        for point in points:
            if point is not None:#maybe some points aren't in the database
                indexes = db.GqlQuery("SELECT __key__ FROM RouteUserPathIndex WHERE points = :1 AND user = :2", point.key(), user.key())
                keys = [k.parent() for k in indexes]#we got the keys from all the RouteUserPath objects
                paths = db.get(keys)#load all the objects (we only have the keys)
                for path in paths:
                    if str(path.path.key()) in possiblePaths:#get the key for the RoutePath instance 
                        possiblePaths[str(path.path.key())] += 1
                    else:
                        possiblePaths[str(path.path.key())] = 1
        return possiblePaths
    
    def get_or_insert(self, user, points):
        """From list of :class:`db.GeoPt` points, returns or create the :class:`RouteUserPath`
        
            :param point: point searching
            :type point: :class:`db.GeoPt`
            :returns: :class:`RouteUserPath`
        """
        path = RoutePath.objects.get_or_insert([p.point for p in points])
        rupa = self.get(user, path)
        if rupa is None:
            rupa = RouteUserPath.get_or_insert(key_name='rupa%s%s' % (str(user.key()), str(path.encodedPoints)), user=user, path=path)
            rupaIndex = RouteUserPathIndex.get_or_insert(key_name='rupai%s%s' % (str(user.key()), str(path.encodedPoints)), parent=rupa, user=user, points=[p.key() for p in points])
        return rupa#the routeuserpath exists, no need to create a new one
           
class RouteUserPath(HookedModel):
    """Describes all the points doing a path, the user who does the path, also saves the total times the path has been correctly predicted"""
    user = db.ReferenceProperty(User, required=True)
    """owner reference"""
    path = db.ReferenceProperty(RoutePath, required=True)
    """class:`RoutePath` reference"""
    created = db.DateTimeProperty(auto_now_add=True)
    """The date of creation"""
    objects = RouteUserPathHelper()
    
    def _pre_put(self):
        """The original path can't be changed"""
        if self.is_saved():
            if self.path.key != self._entity['path']:
                raise NoChanges()
    
    @property
    def points(self):
        """Returns a list with all the points in the path"""
        indexes = db.query_descendants(self)
        if indexes.count() == 0:
            raise db.InternalError('Index doesn\'t exist')
        # seria mejor hacer un get() con la lista de cada index en vez de uno agrupando todas las listas
        return RouteUserPoint.get(reduce(list.__add__,[index.points for index in indexes]))
    
    @property
    def total(self):
        """The total time this point gets visited"""
        return RouteCounter.get_count(self.key())

    def inc_total(self, value=1):
        """Increases the total times this point gets visited
        
            :param value: value to increases
            :type value: integer
        """
        if value <= 0:
            raise db.BadValueError()
        if value == 1:
            RouteCounter.increase_counter(self.key())
        else:
            for i in xrange(1, value):
                RouteCounter.increase_counter(self.key())
                
    def delete(self):
        indexes = db.query_descendants(self)
        for index in indexes:
            index.delete()
        super(self.__class__, self).delete()

