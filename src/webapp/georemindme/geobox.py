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
#===============================================================================
# Code based on: 
# http://code.google.com/intl/es-ES/appengine/articles/geosearch.html
# http://code.google.com/p/google-app-engine-samples/source/browse/trunk/24hrsinsf/geobox.py?r=111
# 
#       from bslatkin@gmail.com (Brett Slatkin)
#===============================================================================

from google.appengine.ext.db import BadValueError
import decimal

# (slice, resolution)
'''
  (10,4),
  (7,4),
  (5,4),
  (3,4),
  (0,4),
  (2,3),
  (5,3),
  (6,3),
  (8,3),
  (1,2),
  (3,2),
  (5,2),
  (7,2),
  (10,2),
  (12,2),
  (15,2),
'''
GEOBOX_CONFIGS = (
  (1, 3),
  (2, 3),
  (3, 3),
  (4, 3),
  (5, 3),
  (6, 3),
  (7, 3),
  (8, 3),
  (9, 3),
  (0, 3),
  (1, 1),
  (2, 1),
  (3, 1),
  (4, 1),
  (5, 1),
  (6, 1),
  (7, 1),
  (8, 1),
  (9, 1),
  (0, 1),
)

def proximity_alerts(user, lat, lon, page=1):
    '''
        Search the alerts near to lat,lon,
        checks the distance from user and alert.
        Return a list of Alert objects
    '''
    alerts = proximity_alerts_all(user, lat, lon, page=page)
    result = []
    for alert in alerts:
        if alert.get_distance() == 0 or _get_distance(lat, lon, alert.poi.point.lat, alert.poi.point.lon) <= alert.get_distance():
            result.append(alert)
    return result

def proximity_alerts_all(user, lat, lon, page=1):
    '''
        Search all the alerts near to lat,lon
        Return a list of Alert objects
    '''
    from models import Alert
    alerts = Alert.objects.get_by_user(user, page)
    boxes = frozenset(generate_geoboxes(lat, lon)) # frozenset has intersection()
    result = []
    
    """if alerts is None:
        return []"""
    
    for alert in alerts:
        if boxes.intersection(alert.poi.geoboxes):
                result.append(alert)
    return result

def generate_geoboxes(lat, lon):
    '''
        Generate a list of geoboxes
        lat: latitude
        lon: longitude
        
        returns list of geoboxes
    '''
    if lat is None or lon is None:
        raise BadValueError()
    list = []
    for slice, resolution in GEOBOX_CONFIGS:
        list.extend(_get_geobox(lat, lon, slice, resolution))
    return sorted(list)

    '''
    distances = ()
    for alert in alerts:
        distance = _get_distance(lat, lon, alert.poi.x, alert.poi.y)
        distances.append((distance, alert))
    distances.sort()
    '''
    

def _get_distance(lat1, lon1, lat2, lon2):
    import math
    
    degtorad = 0.01745329
    radtodeg = 57.29577951
    
    longs = float(lon1) - float(lon2)
 
    #formula para la distancia
    distance = (math.sin(float(lat1) * degtorad) * math.sin(float(lat2) * degtorad)) + (math.cos(float(lat1) * degtorad) * math.cos(float(lat2) * degtorad) * math.cos(longs * degtorad))
   
    distance = math.acos(distance) * radtodeg
    m = (distance * 111.302) * 1000 #cambia a metros
    
    return m
    
def _get_geobox(lat, lon, slice, resolution, accurate=False):
    '''
        Generates a new geobox
    '''
    decimal.getcontext().prec = resolution + 3
    lat = decimal.Decimal(str(lat))
    lon = decimal.Decimal(str(lon))
    slice = decimal.Decimal(str(slice * pow(decimal.Decimal(repr(10)), -resolution))) 
    
    rlat = _round_number_down(lat, slice)
    rlon = _round_number_down(lon, slice)
    
    list = [(_format((rlat, rlon - slice, rlat - slice, rlon), resolution))]
    
    if accurate:
        #to avoid loops, only adds one proximity geobox

        """
         _______    Point near bottom or top
        |     x |
        |       |
        |       |
        |_____x_|
        """
        list.extend(_get_geobox(rlat + slice, rlon, slice, resolution, accurate=False))

        """
         _______    Point near bottom or top
        |       |
        |       |
        |       |
        |_____x_|
        """
        list.extend(_get_geobox(rlat - slice, rlon, slice, resolution, accurate=False))


        """
         _______
        |       |    Point near left
        |x      |
        |       |
        |_______|
        """
        list.extend(_get_geobox(rlat, rlon - slice, slice, resolution, accurate=False))
        
        """
         _______
        |       |    Point near right
        |      x|
        |       |
        |_______|
        """
        list.extend(_get_geobox(rlat, rlon + slice, slice, resolution, accurate=False))
    
    return list

def _format(geobox, resolution):
    format = '%%0.%df' % resolution
    return u"|".join(format % coord for coord in geobox)
        
def _round_number_down(number, slice):
    '''
        round down a number to its slice
    '''
    try:
        r = number % slice
        if number > 0:
            return number - r + slice
        else:
            return number - r
    except:
        return number

