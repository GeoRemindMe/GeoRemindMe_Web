# coding=utf-8

import unittest
from geoalert.models import *
from geoalert.models_poi import *


class Test(unittest.TestCase):
    def test_poi(self):
        u = User.register(email='test@test.com', password='123456', username='usertest')
        u2 = User.register(email='test2@test.com', password='123456', username='usertest2')
        #crear privateplace
        self.assertRaises(AttributeError, PrivatePlace.get_or_insert,id = None, name=None, bookmark=False, address = None,
                         business = None, location = None, user = None), 'No deberia crearse el PrivatePlace'
        self.assertRaises(AttributeError, PrivatePlace.get_or_insert,id = None, name=None, bookmark=False, address = None,
                         business = None, location = None, user = u), 'No deberia crearse el PrivatePlace'
        self.assertRaises(AttributeError, PrivatePlace.get_or_insert,id = None, name=None, bookmark=False, address = None,
                         business = None, location = '1,2', user = None), 'No deberia crearse el PrivatePlace'
        assert isinstance(PrivatePlace.get_or_insert(id = None, name=None, bookmark=False, address = None,
                         business = None, location = '1,2', user = u), PrivatePlace), 'Error creando el PrivatePlace'
        assert isinstance(PrivatePlace.get_or_insert(id = None, name=None, bookmark=False, address = None,
                         business = None, location = db.GeoPt(1,2), user = u), PrivatePlace), 'Error creando el PrivatePlace'
        self.assertRaises(AttributeError, PrivatePlace.get_or_insert, id = None, name=None, bookmark=False, address = 111,
                         business = None, location = '1,2', user = u), 'No deberia crearse el PrivatePlace'
        self.assertRaises(AttributeError, PrivatePlace.get_or_insert, id = None, name=12, bookmark=False, address = None,
                         business = None, location = '1,2', user = u), 'No deberia crearse el PrivatePlace'
        
        
    def test_alert(self):
        u = User.register(email='test@test.com', password='123456', username='usertest')
        u2 = User.register(email='test2@test.com', password='123456', username='usertest2')
        poi = PrivatePlace.get_or_insert(id = None, name=None, bookmark=False, address = None, business = None, location = '1,2', user = u)
        #crear alerta
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = None, description = None,
                                                                  date_starts = None, date_ends = None, poi = None,
                                                                  user = None, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = None, description = None,
                                                                  date_starts = None, date_ends = None, poi = None,
                                                                  user = u, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = None, description = None,
                                                                  date_starts = None, date_ends = None, poi = poi,
                                                                  user = None, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = 123, description = None,
                                                                  date_starts = None, date_ends = None, poi = poi,
                                                                  user = u, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = '', description = 123,
                                                                  date_starts = None, date_ends = None, poi = poi,
                                                                  user = u, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(BadValueError, Alert.update_or_insert, id = None, name = 'asdf', description = None,
                                                                  date_starts = 1231, date_ends = None, poi = poi,
                                                                  user = u, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        self.assertRaises(AttributeError, Alert.update_or_insert, id = None, name = None, description = None,
                                                                  date_starts = None, date_ends = 1234, poi = poi,
                                                                  user = u, done = False, active = None, done_when=None), 'No deberia crearse la alerta'
        
        assert isinstance(Alert.update_or_insert(id = None, name = 'alerta', description = None,
                                                date_starts = None, date_ends = None, poi=poi,
                                                user = u, active=None, done_when=None), Alert), 'Error creando la alerta'
        assert isinstance(Alert.update_or_insert(id = None, name = 'alerta', description = 'DESC',
                                                date_starts = None, date_ends = None, poi=poi,
                                                user = u, active=None, done_when=None), Alert), 'Error creando la alerta'
        assert isinstance(Alert.update_or_insert(id = None, name = 'alerta', description = 'DESC',
                                                date_starts = None, date_ends = None, poi=poi,
                                                user = u, active=None, done_when=None), Alert), 'Error creando la alerta'
        