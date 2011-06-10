# coding=utf-8

from django.utils.translation import ugettext as _
from google.appengine.ext import db, search
from google.appengine.ext.db import polymodel

from geomodel.geomodel import GeoModel
from georemindme.decorators import classproperty
from georemindme.models_utils import Visibility
from geouser.models import User
from signals import *


class Business(db.Model):
    '''Nombres genericos para un place (farmacia, supermercado, ...)'''
    name = db.StringProperty()
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [['name']]
    


class POI(polymodel.PolyModel, search.SearchableModel, GeoModel):
    ''' Puntos de interes '''
    name = db.StringProperty()
    bookmark = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    users = db.ListProperty(db.Key)  #  lista con los usuarios que han modificado el POI
    user = db.ReferenceProperty(User)  # el usuario que creo el POI
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [[],['name']]
    
    @property
    def id(self):
        return self.key().id()
    
    @classproperty
    def objects(self):
        return POIHelper()


class PrivatePlace(POI):
    '''Lugares especificos para una alerta, solo visibles por el usuario que los crea'''
    address = db.StringProperty()
    business = db.ReferenceProperty(Business)
    google_places_id = db.StringProperty(default=None) 
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [ ['address'], ['business'], ['point'], ['name', 'address', 'business', 'point']]
    
    @classproperty
    def objects(self):
        return PrivatePlaceHelper()
    
    @classmethod
    def get_or_insert(cls, id = None, name = None, bookmark = False, address = None,
                         business = None, google_places_id = None, location = None, user = None):
        if id:
            place = cls.objects.get_by_id(id, user)
        else:
            place = cls.objects.get_by_address_or_point_user(address, user, location = location)
            if place is None:
                place = PrivatePlace(name = name, bookmark = bookmark,
                                 address = address, business = business,
                                 google_places_id = google_places_id,
                                 location = location, user = user)
                place.put()
        return place
            
    
    def put(self):
        self.update_location()
        if self.is_saved():
            super(self.__class__, self).put()
            place_modified.send(sender=self)
        else:
            super(self.__class__, self).put()
            place_new.send(sender=self)
        
        
    def delete(self):
        place_deleted.send(sender=self)
        super(PrivatePlace, self).delete()

    
class Place(PrivatePlace):
    '''Lugares para una alerta, visibles para todos'''
    
    @classproperty
    def objects(self):
        return PlaceHelper()
    
    def delete(self):
        pass
    
from helpers_poi import *