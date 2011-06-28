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
        return PrivatePlace.objects.get_by_business_user(self, user, page=page, query_id=query_id)
    
    def get_places(self, page=1, query_id=None):
        """
            Obtiene una lista de lugares publicos con este tipo de negocio
        """
        return Place.objects.get_by_business(self, page=page, query_id=query_id)
    


class POI(polymodel.PolyModel, search.SearchableModel, GeoModel):
    ''' Puntos de interes '''
    name = db.StringProperty()
    bookmark = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    users = db.ListProperty(db.Key)  #  lista con los usuarios que han modificado el POI
    user = db.ReferenceProperty(User, required=False)  # el usuario que creo el POI
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
        """
            Obtiene o añade un nuevo punto a la BD
            
                :param id: identificador del punto (opcional)
                :type id: :class:`integer`
                :param name: nombre para identificar el punto (opcional)
                :type name: :class:`string`
                :param bookmark: marca el punto como favorito
                :type bookmark: :class:`boolean`
                :param business: tipo de negocio (opcional)
                :type business: :class:`geoalert.models_poi.Business`
                :param location: coordenadas del punto
                :type location: :class:`db.GeoPt` o :class:string`
                :param user: usuario que añade o busca el punto
                :type user: :class:`geouser.models.User`
                
                :returns: :class:`geoalert.models_poi.PrivatePlace`
                :raises: AttributeError
        """
        if id:
            place = cls.objects.get_by_id_user(id, user)
        else:
            if name is not None and not isinstance(name, basestring):
                raise AttributeError()
            if address is not None and not isinstance(address, basestring):
                raise AttributeError()
            if business is not None and not isinstance(business, Business):
                raise AttributeError()
            place = cls.objects.get_by_address_or_point_user(address, user, location = location)
            if place is None:
                if location is None or user is None:
                    raise AttributeError()
                place = PrivatePlace(name = name, bookmark = bookmark,
                                 address = address, business = business,
                                 location = location, user = user)
                place.put()
        return place
    
    @classmethod
    def insert_or_update(cls, id = None, name = None, bookmark = False, address = None,
                         business = None, location = None, user = None):
        """
            Añade o actualiza un nuevo punto a la BD
            
                :param id: identificador del punto (opcional)
                :type id: :class:`integer`
                :param name: nombre para identificar el punto (opcional)
                :type name: :class:`string`
                :param bookmark: marca el punto como favorito
                :type bookmark: :class:`boolean`
                :param business: tipo de negocio (opcional)
                :type business: :class:`geoalert.models_poi.Business`
                :param location: coordenadas del punto
                :type location: :class:`db.GeoPt` o :class:string`
                :param user: usuario que añade o busca el punto
                :type user: :class:`geouser.models.User`
                
                :returns: :class:`geoalert.models_poi.PrivatePlace`
                :raises: AttributeError
        """
        if id:
            place = cls.objects.get_by_id_user(id, user)
            if place is not None:
                place.update(name = name, bookmark = bookmark,
                             address = address, business = business,
                             location = location)    
        else:
            place = cls.objects.get_by_address_or_point_user(address, user, location = location)
            if place is None:
                if name is not None and not isinstance(name, basestring):
                    raise AttributeError()
                if address is not None and not isinstance(address, basestring):
                    raise AttributeError()
                if business is not None and not isinstance(business, Business):
                    raise AttributeError()
                if location is None or user is None:
                    raise AttributeError()
                place = PrivatePlace(name = name, bookmark = bookmark,
                                 address = address, business = business,
                                 location = location, user = user)
                place.put()
        return place
    
    def update(self, name = None, bookmark = False, address = None, business = None, location = None):
        if location is None:
            raise AttributeError()
        if name is not None and not isinstance(name, basestring):
            raise AttributeError()
        if address is not None and not isinstance(address, basestring):
            raise AttributeError()
        if business is not None and not isinstance(business, Business):
            raise AttributeError()
        
        self.name = name
        self.bookmark = bookmark
        self.address = address
        self.business = business
        self.location = db.GeoPt(location)
        self.put()
            
    
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
    def insert_or_update_google(cls, name, address, city, location, google_places_reference, google_places_id, user):
        """
            Añade o actualiza un nuevo punto publico a la BD
            
                :param name: nombre para identificar el punto (opcional)
                :type name: :class:`string`
                :param city: ciudad donde esta el punto
                :type city: :class:`string`
                :param location: coordenadas del punto
                :type location: :class:`db.GeoPt` o :class:string`
                :param google_places_reference: referencia devuelta por google places
                :type google_places_reference: :class:`string`
                :param google_places_id: id devuelto por google places
                :type google_places_id: :class:`string`
                :param user: usuario que añade o busca el punto por primera vez
                :type user: :class:`geouser.models.User`
                
                :returns: :class:`geoalert.models_poi.PrivatePlace`
                :raises: AttributeError
        """

        place = cls.objects.get_by_google_id(google_places_id)
        if not isinstance(location, db.GeoPt):
            location = db.GeoPt(location)
        if place is not None:
            place.update(name, address, city, location, google_places_reference, google_places_id)    
        else:
            place = Place(name=name, address=address,
                          city=city, location=location, 
                          google_places_reference=google_places_reference,
                          google_places_id=google_places_id, user=user)
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
        """
            Añade el punto a la tabla en fusiontables
            
            En caso de fallo, se guarda el punto en _Do_later_ft,
            para intentar añadirlo luego
        """
        from mapsServices.fusiontable import ftclient, sqlbuilder
        from django.conf import settings
        try:
            ftclient = ftclient.OAuthFTClient()
            ftclient.query(sqlbuilder.SQL().insert(settings.FUSIONTABLES['TABLE_PLACES'],
                                                    {'bus_id': self.business.id if self.business is not None else -1,
                                                    'location': '%s,%s' % (self.location.lat, self.location.lon),
                                                    'place_id': self.id,
                                                    'modified': self.modified.__str__(),
                                                     }
                                                   )
                           )
        except:  # Si falla, se guarda para intentar añadir mas tarde
            from georemindme.models_utils import _Do_later_ft
            later = _Do_later_ft(instance_key=self.key())
            later.put()

from helpers_poi import *