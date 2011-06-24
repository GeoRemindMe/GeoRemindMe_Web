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
    
    @classproperty
    def objects(self):
        return BusinessHelper()
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [['name']]
    
    def get_privateplaces(self, user, page=1, query_id=None):
        """
            Obtiene una lista de lugares privados del usuario con este negocio
        """
        return PrivatePlaces.objects.get_by_business_user(self, user, page=page, query_id=query_id)
    
    def get_places(self, page=1, query_id=None):
        """
            Obtiene una lista de lugares publicos con este tipo de negocio
        """
        return Places.objects.get_by_business(self, page=page, query_id=query_id)
    


class POI(polymodel.PolyModel, search.SearchableModel, GeoModel):
    ''' Puntos de interes '''
    name = db.StringProperty()
    bookmark = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    users = db.ListProperty(db.Key)  #  lista con los usuarios que han modificado el POI
    user = db.ReferenceProperty(User)  # el usuario que creo el POI
    address = db.StringProperty()
    
    
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
    business = db.ReferenceProperty(Business)
    
    
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
                         business = None, location = None, user = None):
        if id:
            place = cls.objects.get_by_id(id, user)
        else:
            place = cls.objects.get_by_address_or_point_user(address, user, location = location)
            if place is None:
                place = PrivatePlace(name = name, bookmark = bookmark,
                                 address = address, business = business,
                                 location = location, user = user)
                place.put()
        return place
            
    
    def put(self):
        self.update_location()
        if self.is_saved():
            super(PrivatePlace, self).put()
            privateplace_modified.send(sender=self)
        else:
            super(PrivatePlace, self).put()
            privateplace_new.send(sender=self)
        
        
    def delete(self):
        privateplace_deleted.send(sender=self)
        super(PrivatePlace, self).delete()
        
    def insert_ft(self):
        from mapsServices.fusiontable import ftclient, sqlbuilder
        from django.conf import settings

        ftclient = ftclient.ClientLoginFTClient()
        ftclient.query(sqlbuilder.SQL().insert(settings.FUSIONTABLES['TABLE_PLACES'],
                                                {
                                                 'bus_id': '',
                                                 'location': self.location.__str__(),
                                                 'place_id': self.key().id(),
                                                 'modified': self.modified.__str__()
                                                 }
                                               )
                       )

    
class Place(POI):
    '''Lugares para una alerta, visibles para todos'''
    slug = db.StringProperty()
    city = db.TextProperty()
    google_places_reference = db.StringProperty()
    google_places_id = db.StringProperty(default=None)
    business = db.ReferenceProperty(Business)
 
    
    @classproperty
    def objects(self):
        return PlaceHelper()

    
    def delete(self):
        pass
 
    
    def put(self):
        """
            Comprueba que el slug es unico
        """
        from georemindme.funcs import u_slugify
        if self.slug is None:
            self.slug = u_slugify('%s-%s'% (self.name, self.city))
        p = Place.all().filter('slug =', self.slug).get()
        if p is not None:
            if not self.is_saved() or p.key() != self.key():
                i = 1
                while p is not None:
                    slug = self.slug + '-%s' % i
                    p = Place.all().filter('slug =', slug).get()
                self.slug = self.slug + '-%s' % i
        if self.is_saved():
            super(Place, self).put()
            place_modified.send(sender=self)
        else:
            super(Place, self).put()
            place_new.send(sender=self)
        
    def get_absolute_url(self):
        return '/place/%s' % self.slug
    
    
    @classmethod
    def insert_or_update(cls, name, address, city, location, google_places_reference, google_places_id):
        place = cls.objects.get_by_google_id(google_places_id)
        if place is not None:
            place.update(name, address, city, location, google_places_reference, google_places_id)    
        else:
            place = Place(name=name, address=address,
                          city=city, location=location, 
                          google_places_reference=google_places_reference,
                          google_places_id=google_places_id)
            place.put()
        return place
        
    def update(self, name, address, city, location, google_places_reference, google_places_id):
        self.name = name
        self.address = address
        self.city = city
        self.location = location
        self.google_places_reference = google_places_reference
        self.google_places_id = google_places_id
        self.put()
        
    def insert_ft(self):
        from mapsServices.fusiontable import ftclient, sqlbuilder
        from django.conf import settings
        try:
            ftclient = ftclient.ClientLoginFTClient()
            ftclient.query(sqlbuilder.SQL().insert(settings['TABLE_PLACES'], {'bus_id': self.business,
                                                                            'location': '%s,%s' % (self.location.lat, self.location.lon),
                                                                            'place_id': self.id,
                                                                             }
                                                   )
                           )
        except:
            # TODO :  guardar recordatorio por si fallo añadir el sitio
            pass
            #__do_later(self.kind(), self.key())
            #__do_later.put()

from helpers_poi import *