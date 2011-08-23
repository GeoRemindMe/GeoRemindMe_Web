# coding=utf-8

from django.utils.translation import gettext_lazy as _
from google.appengine.ext import db, search
from google.appengine.ext.db import polymodel

from geomodel.geomodel import GeoModel
from georemindme.decorators import classproperty
from georemindme.models_utils import Visibility
from geouser.models import User
from signals import *

def _get_city(components):
    if components is None:
        return None
    for i in components:
        if 'locality' in i['types']:
            return i['short_name']
        
        
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
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User, required=False)  # el usuario que creo el POI
    address = db.StringProperty()
    
    
    @classmethod
    def SearchableProperties(cls):
        '''
        Por defecto, SearchableModel indexa todos las propiedades de texto
        del modelo, asi que aqui indicamos las que realmente necesitamos
        '''
        return [ ['address'], ['business'], ['point'], ['name', 'address', 'business', 'point']]
    
    
    @property
    def id(self):
        return self.key().id()
    
    
    @classproperty
    def objects(self):
        return POIHelper()
    
    def to_dict(self):
        import time
        return {'id': self.id,
                'name': self.name,
                'x': self.location.lat,
                'y': self.location.lon,
                'address': unicode(self.poi.address),
                'created': self.created if self.created is not None else 0,
                }


class PrivatePlace(POI):
    '''Lugares especificos para una alerta, solo visibles por el usuario que los crea'''
    business = db.ReferenceProperty(Business)
    bookmark = db.BooleanProperty(default=False)
    
    
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
            
    
    def put(self, from_comment=False):
        self.update_location()
        if self.is_saved():
            super(PrivatePlace, self).put()
            if from_comment:
                return self
            privateplace_modified.send(sender=self)
        else:
            super(PrivatePlace, self).put()
            from watchers import new_place
            privateplace_new.send(sender=self)
        
        
    def delete(self):
        privateplace_deleted.send(sender=self)
        super(PrivatePlace, self).delete()
        
    def to_dict(self):
        import time
        return {'id': self.id,
                'name': self.name,
                'x': self.location.lat,
                'y': self.location.lon,
                'business': self.business.name if self.business is not None else None,
                'address': unicode(self.address),
                'created': self.created if self.created is not None else 0,
                }
        
    def __str__(self):
        if self.name is not None:
            return unicode(self.name).encode('utf-8')
        else:
            return str(self.id)

    def __unicode__(self):
        if self.name is not None:
            return self.name
        else:
            return unicode(self.id)

    
class Place(POI):
    '''Lugares para una alerta, visibles para todos'''
    slug = db.StringProperty()
    city = db.TextProperty()
    google_places_reference = db.StringProperty()
    google_places_id = db.StringProperty()
    foursquare_id = db.StringProperty()
    business = db.ReferenceProperty(Business)
    users = db.ListProperty(db.Key)  #  lista con los usuarios que administran el POI
 
    
    @classproperty
    def objects(self):
        return PlaceHelper()

    
    def delete(self):
        pass
 
    
    def put(self, from_comment=False):
        """
            Comprueba que el slug es unico
        """
        if from_comment:
            super(Place, self).put()
            return self
        from django.template.defaultfilters import slugify
        if self.slug is None:
            name = self.name.lower()
            if self.city is not None:
                city = self.city.lower()
                self.slug = unicode(slugify('%s-%s'% (name, city)))
            else:
                self.slug = unicode(slugify('%s' % name))
                self.city = name
        p = Place.all().filter('slug =', self.slug).get()
        if p is not None:
            if not self.is_saved() or p.key() != self.key():
                i = 1
                while p is not None:
                    slug = self.slug + '-%s' % i
                    p = Place.all().filter('slug =', slug).get()
                self.slug = self.slug + '-%s' % i
        if self.is_saved():
            place_modified.send(sender=self)
        else:
            super(Place, self).put()
            place_new.send(sender=self)
        

    def get_absolute_url(self):
        return '/place/%s/' % self.slug
    
    def get_absolute_fburl(self):
        return '/fb%s' % self.get_absolute_url()
    
    
    @classmethod
    def insert_or_update_google(cls, user, google_places_reference=None, name=None, address=None, city=None, location=None, google_places_id=None):
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
        if google_places_id is None and google_places_reference is not None:
                from mapsServices.places.GPRequest import GPRequest
                try:
                    search = GPRequest().retrieve_reference(google_places_reference)
                    return Place.insert_or_update_google(name=search['result']['name'],
                                address=search['result'].get('formatted_address'), 
                                city=_get_city(search['result'].get('address_components')),
                                location=db.GeoPt(search['result']['geometry']['location']['lat'], search['result']['geometry']['location']['lng']),
                                google_places_reference=search['result']['reference'],
                                google_places_id=search['result']['id'],
                                user = user
                                )
                except:
                    return None
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
    
#    @classmethod
#    def insert_or_update_foursquare(cls, user, foursquare_id):
#        place = cls.objects.get_by_foursquare_id(foursquare_id)
#        from mapsServices.places.FSRequest import FSRequest
#        search = FSRequest().retrieve_reference(foursquare_id)
#        if place is not None:
#            place.update(name=search['name'], 
#                         address=search['location'].get('address', ''), 
#                         city=search['location'].get('city', ''), 
#                         location=db.GeoPt(search['location'].get('lat', 0), search['location'].get('lng', 0))
#                         )    
#        else:    
#            place = Place(name=search['name'], 
#                         address=search['location'].get('address', ''), 
#                         city=search['location'].get('city', ''), 
#                         location=db.GeoPt(search['location'].get('lat', 0), search['location'].get('lng', 0))
#                         )
#            place.put()
#        return place
    
    def update(self, name, address, city, location, google_places_reference, google_places_id):
        self.name = name
        if address is not None:
            self.address = address
        if city is not None:
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
            
    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'x': self.location.lat,
                'y': self.location.lon,
                'business': self.business.name if self.business is not None else None,
                'address': unicode(self.address),
                'created': self.created if self.created is not None else 0,
                }
        
    def __str__(self):
        if self.name is not None:
            return unicode(self.name).encode('utf-8')
        else:
            return str(self.id)

    def __unicode__(self):
        if self.name is not None:
            return self.name
        else:
            return unicode(self.id)

from helpers_poi import *
