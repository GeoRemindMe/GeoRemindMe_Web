# coding=utf-8

from google.appengine.ext import db

from models_poi import *
from exceptions import ForbiddenAccess
from georemindme.paging import *
from geouser.models import User


class POIHelper(object):
    _klass = POI
    
    def get_by_id(self, id):
        try:
            id = long(id)
        except:
            return None
        return self._klass.get_by_id(id)
    
    def search(self, word, page=1, query_id = None):
        q = self._klass.all().search(word).order('-modified')
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id_user(self, id, user):
        if not isinstance(user, User):
            raise AttributeError()
        poi = self.get_by_id(id)
        if poi is None or (poi.user.key() != user.key()):
            return None
        return poi


class PrivatePlaceHelper(POIHelper):
    _klass = PrivatePlace
    
    def get_by_business_user(self, business, user, page=1, query_id=None):
        if not isinstance(user, User):
            raise AttributeError()
        if not isinstance(business, Business):
            raise AttributeError()
        
        q = self._klass.gql('WHERE business = :1 AND user = :2 ORDER BY created DESC', business, user)
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_address_or_point_user(self, address, user, location = None):
        if not isinstance(user, User):
            raise AttributeError()
        if address is not None and address != '':
            if not isinstance(address, basestring):
                raise AttributeError()
            place = self._klass.gql('WHERE address = :1 AND user = :2 ORDER BY created DESC', address, user).get()
            if place is not None:
                return place
        if location is None:
            raise AttributeError()
        location = db.GeoPt(location)
        return self._klass.gql('WHERE location = :1 AND user = :2 ORDER BY created DESC', location, user).get()


class PlaceHelper(POIHelper):
    _klass = Place
    
    def get_by_slug(self, slug):
        if not isinstance(slug, basestring):
            raise AttributeError()
        if slug == '':
            raise AttributeError()
        return self._klass.gql('WHERE slug = :1', slug).get()
    
    def get_by_google_reference(self, reference):
        if not isinstance(reference, basestring):
            raise AttributeError()
        if reference == '' :
            raise AttributeError()
        return self._klass.gql('WHERE google_places_reference = :1', reference).get()
    
    def get_by_google_id(self, id):
        try:
            id = str(id)
        except:
            return None
        if id == '' :
            raise AttributeError()
        return self._klass.gql('WHERE google_places_id = :1', id).get()


class BusinessHelper(object):
    def get_by_name(self, business):
        if not isinstance(business, basestring):
            raise AttributeError()

        return Business.all().filter('name =', business).get()
    
