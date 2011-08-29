import unittest
from georoute.models import *


class Test(unittest.TestCase):
    def test_routepoint(self):
        #check point
        assert RoutePoint.objects.get_point(db.GeoPt(1.1,1.1))==None, 'Point cannot exists'
        #add point
        assert isinstance(RoutePoint.objects.get_or_insert(point=db.GeoPt(1.1,1.1)),RoutePoint), 'Cannot create point'
        assert isinstance(RoutePoint.objects.get_point(db.GeoPt(1.1,1.1)),RoutePoint), 'Cannot find point'
        assert isinstance(RoutePoint.objects.get_or_insert(point=db.GeoPt(2.2,2.2)),RoutePoint), 'Cannot create point'
        #get lists of points
        assert type(RoutePoint.objects.get_points([db.GeoPt(1.1,1.1), db.GeoPt(2.2,2.2)])).__name__ == 'list', 'Cannot find list of points'
        assert len(RoutePoint.objects.get_points([db.GeoPt(1.1,1.1), db.GeoPt(2.2,2.2)])) == 2, 'Cannot find two points'
        assert RoutePoint.objects.get_points([db.GeoPt(1.1,1.1), db.GeoPt(2.2,2.2), db.GeoPt(3.3,3.3)])[2] == None, 'Found a 3rd point0'
        #delete points
        RoutePoint.objects.get_point(db.GeoPt(1.1,1.1)).delete()
        assert RoutePoint.objects.get_point(db.GeoPt(1.1,1.1))==None, 'Point cannot exists'
        RoutePoint.objects.get_point(db.GeoPt(2.2,2.2)).delete()
        assert RoutePoint.objects.get_point(db.GeoPt(2.2,2.2))==None, 'Point cannot exists'
        
        
