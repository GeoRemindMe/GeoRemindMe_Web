# coding=utf-8

import unittest
from geouser.models import *
from django.core.exceptions import ValidationError
from google.appengine.ext import db


class Test(unittest.TestCase):
    def test_user(self):
        #crea un usuario (usertest y usertest2), usertest3 lo crea y lo borra
        assert isinstance(User.register(email='test@test.com', password='123456', username='usertest'), User), 'No se puede crear el usuario'
        assert isinstance(User.register(email='test2@test.com', password='123456', username='usertest2'), User), 'No se puede crear el usuario'
        assert isinstance(User.register(email='test3@test.com', password='123456', username='usertest3'), User), 'No se puede crear el usuario'
        assert isinstance(User.objects.get_by_email('test3@test.com'), User), 'No se puede encontrar al usuario'
        assert User.objects.get_by_email('test3@test.com').delete()==None, 'No se pudo borrar el usuario'
        assert isinstance(User.register(email='test4@test.com', password='123456'), User), 'No se puede crear el usuario'
        
        #intenta registrar con email erroneo
        self.assertRaises(ValidationError, User.register, email='test @test.com', password='123456', username='usertest')
        
        #intenta registrar con mismo email 
        self.assertRaises(User.UniqueEmailConstraint, User.register, email='test@test.com', password='123456', username='usertest')
        
        #intenta registrar con mismo username
        self.assertRaises(User.UniqueUsernameConstraint, User.register, email='test3@test.com', password='123456', username='usertest')
        
        #intenta registrar con password invalido
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123 456', username='usertest1')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123@456', username='usertest1')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='1234567890123456', username='usertest1')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123', username='usertest1')
        
        #intenta registrar con username invalido
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123456', username=' usertest1')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123456', username='#usertest1')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123456', username='us')
        self.assertRaises(ValueError, User.register, email='test3@test.com', password='123456', username='')
        
        #cambiar configuracion de usuario
        u = User.objects.get_by_email('test@test.com')
        self.assertRaises(User.UniqueEmailConstraint, u.update, email='test2@test.com')
        self.assertRaises(ValidationError, u.update, email='test @test.com')
        assert u.email == 'test@test.com', 'Email no deberia haber cambiado'
        assert u.update(email='test@test.com'), 'Deberia poderse cambiar con mismo email'
        self.assertRaises(User.UniqueUsernameConstraint, u.update, username='usertest2')
        assert u.username == 'usertest', 'Username no deberia haber cambiado'
        assert u.update(username='usertest'), 'Deberia poderse cambiar con mismo email'
        assert u.update(email='test3@test.com'), 'Deberia poderse cambiar email'
        assert u.update(username='usertest3'), 'Deberia poderse cambiar nombre usuario'
        #self.assertRaises(ValueError, u.update, password='usertest2')
        #self.assertRaises(ValueError, u.update, password='usertest2', oldpassword='1231111')
        assert u.update(password='111111', oldpassword='123456'), 'No se pudo cambiar el password'
        assert u.update(username='usertest', email='test@test.com', password=123456, oldpassword=111111), 'No se puedo volver a datos iniciales'
        assert u.check_password(123456), 'No se puedo volver a datos iniciales'
    
    
    def test_userhelper(self):
        #probar todas las busquedas en helper
        User.register(email='test@test.com', password='123456', username='usertest')
        User.register(email='test2@test.com', password='123456', username='usertest2')
        u = User.objects.get_by_email('test@test.com')
        assert User.objects.get_by_key(u.key()).id == u.id, 'Busqueda por key erronea'
        assert User.objects.get_by_key(str(u.key())).id == u.id, 'Busqueda por string de key erronea'
        assert User.objects.get_by_key('asdf') == None, 'Busqueda por key erronea'
        assert User.objects.get_by_key('') == None, 'Busqueda por key erronea'
        assert User.objects.get_by_key(None) == None, 'Busqueda por key erronea'
        assert User.objects.get_by_key(1111) == None, 'Busqueda por key erronea'
        
        assert User.objects.get_by_username(u.username).id == u.id, 'Busqueda por username erronea'
        assert User.objects.get_by_username(u.username, keys_only=True) == u.key(), 'Busqueda por username erronea'
        assert User.objects.get_by_username('asdf')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_username('')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_username(None)== None, 'Busqueda por username erronea'
        
        assert User.objects.get_by_id(u.id).id == u.id, 'Busqueda por username erronea'
        assert User.objects.get_by_id(u.id, keys_only=True) == u.key(), 'Busqueda por username erronea'
        assert User.objects.get_by_id('asdf')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_id('')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_id(123)== None, 'Busqueda por username erronea'
        assert User.objects.get_by_id(None)== None, 'Busqueda por username erronea'
        
        assert User.objects.get_by_email(u.email).id == u.id, 'Busqueda por username erronea'
        assert User.objects.get_by_email(u.email, keys_only=True) == u.key(), 'Busqueda por username erronea'
        assert User.objects.get_by_email('asdf')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email('')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email(123)== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email(None)== None, 'Busqueda por username erronea'
        
        assert User.objects.get_by_email_not_confirm(u.email).id == u.id, 'Busqueda por username erronea'
        assert User.objects.get_by_email_not_confirm(u.email, keys_only=True) == u.key(), 'Busqueda por username erronea'
        assert User.objects.get_by_email_not_confirm('asdf')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email_not_confirm('')== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email_not_confirm(123)== None, 'Busqueda por username erronea'
        assert User.objects.get_by_email_not_confirm(None)== None, 'Busqueda por username erronea'
        
    def test_follow(self):
        User.register(email='test@test.com', password='123456', username='usertest')
        User.register(email='test2@test.com', password='123456', username='usertest2')
        u = User.objects.get_by_email('test@test.com')
        u2 = User.objects.get_by_email('test2@test.com')
        assert User.objects.get_followers(userid=u.id)[1] == u.get_followers()[1], 'Busqueda de followers erronea'
        assert User.objects.get_followers(username=u.username)[1] == u.get_followers()[1], 'Busqueda de followers erronea'
        query_id = u.get_followers()[0]
        assert User.objects.get_followers(userid=u.id, query_id=query_id, page=1) == u.get_followers(query_id=query_id, page=1), 'Busqueda de followers erronea'
        assert User.objects.get_followers(username=u.username, query_id=query_id, page=1) == u.get_followers(query_id=query_id, page=1), 'Busqueda de followers erronea'
        
        assert User.objects.get_followings(userid=u.id)[1] == u.get_followings()[1], 'Busqueda de followings erronea'
        assert User.objects.get_followings(username=u.username)[1] == u.get_followings()[1], 'Busqueda de followings erronea'
        query_id = u.get_followings()[0]
        assert User.objects.get_followings(userid=u.id, query_id=query_id, page=1) == u.get_followings(query_id=query_id, page=1), 'Busqueda de followings erronea'
        assert User.objects.get_followings(username=u.username, query_id=query_id, page=1) == u.get_followings(query_id=query_id, page=1), 'Busqueda de followings erronea'
        
        #ahora probamos añadir followers, etc.
        #assert u.add_following(followid=u2.id), 'Error añadiendo following'
        ##assert User.objects.get_followings(userid=u.id)[1] == u.get_followings()[1], 'Busqueda de followings erronea'
        #assert User.objects.get_followings(userid=u.id, query_id=query_id, page=2) != u.get_followings(query_id=query_id, page=1), 'Busqueda de followings erronea'
        #assert u.del_following(followid=u2.id), 'Error borrando following'
        assert User.objects.get_followings(userid=u.id)[1] == u.get_followings()[1], 'Busqueda de followings erronea'
        assert User.objects.get_followings(userid=u.id, query_id=query_id, page=2) == u.get_followings(query_id=query_id, page=1), 'Busqueda de followings erronea'
        assert u.add_following(followname=u2.username), 'Error añadiendo following'
        assert User.objects.get_followers(userid=u.id)[1] == u.get_followers()[1], 'Busqueda de followings erronea'
        assert u.del_following(followname=u2.username), 'Error añadiendo following'
        assert User.objects.get_followers(userid=u.id)[1] == u.get_followers()[1], 'Busqueda de followings erronea'
        
        # añadir dos veces no debe fallar
        assert u.add_following(followname=u2.username), 'Error añadiendo following'
        assert u.add_following(followid=u2.id), 'Error añadiendo following'
        self.assertRaises(AttributeError, u.add_following), 'Error añadiendo following'
        assert u.add_following(followid=12445)==False, 'Error añadiendo following'
        assert u.add_following(followname='')==False, 'Error añadiendo following'

        self.assertRaises(AttributeError, u.del_following), 'Error borrando following'
        assert u.del_following(followid=12445)==False, 'Error borrando following'
        assert u.del_following(followname='')==False, 'Error borrando following'      
        
    def test_acchelper(self):
        #probar todas las busquedas en helper de models_acc
        User.register(email='test@test.com', password='123456', username='usertest')
        User.register(email='test2@test.com', password='123456', username='usertest2')
        u = User.objects.get_by_email('test@test.com')
        assert UserSettings.objects.get_by_id(u.id).key() == u.settings.key(), 'Busqueda de settings erronea'
        assert UserSettings.objects.get_by_id(str(u.id)).key() == u.settings.key(), 'Busqueda de settings erronea'
        assert UserSettings.objects.get_by_id('asdf')== None, 'Busqueda de settings erronea'
        assert UserSettings.objects.get_by_id('')== None, 'Busqueda de settings erronea'
        assert UserSettings.objects.get_by_id(123)== None, 'Busqueda de settings erronea'
        assert UserSettings.objects.get_by_id(None)== None, 'Busqueda de settings erronea'
        
        assert UserProfile.objects.get_by_id(u.id).key() == u.profile.key(), 'Busqueda de profile erronea'
        assert UserProfile.objects.get_by_id(str(u.id)).key() == u.profile.key(), 'Busqueda de profile erronea'
        assert UserProfile.objects.get_by_id('asdf') == None, 'Busqueda de profile erronea'
        assert UserProfile.objects.get_by_id('') == None, 'Busqueda de profile erronea'
        assert UserProfile.objects.get_by_id(123) == None, 'Busqueda de profile erronea'
        assert UserProfile.objects.get_by_id(None) == None, 'Busqueda de profile erronea'

        assert UserCounter.objects.get_by_id(u.id).key() == u.counters.key(), 'Busqueda de contadores erronea'
        assert UserCounter.objects.get_by_id(str(u.id)).key() == u.counters.key(), 'Busqueda de contadores erronea'
        assert UserCounter.objects.get_by_id('asdf')== None, 'Busqueda de contadores erronea'
        assert UserCounter.objects.get_by_id('')== None, 'Busqueda de contadores erronea'
        assert UserCounter.objects.get_by_id(123) == None, 'Busqueda de contadores erronea'
        assert UserCounter.objects.get_by_id(None) == None, 'Busqueda de contadores erronea'
        
        assert UserTimeline.objects.get_by_id(u.id)[1] == u.get_timeline()[1], 'Error en timeline'
        assert UserTimeline.objects.get_by_id(str(u.id))[1] == u.get_timeline()[1], 'Error en timeline'
        assert UserTimeline.objects.get_by_id('asdf') == None, 'Error en timeline'
        assert UserTimeline.objects.get_by_id('') == None, 'Error en timeline'
        assert UserTimeline.objects.get_by_id(123)[1] == [], 'Error en timeline'
        assert UserTimeline.objects.get_by_id(None) == None, 'Error en timeline'
          
        
        
        
        