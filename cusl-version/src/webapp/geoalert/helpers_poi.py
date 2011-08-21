# coding=utf-8

from google.appengine.ext import db

from models_poi import *
from exceptions import ForbiddenAccess
from georemindme.paging import *
from geouser.models import User

class POIHelper(object):
    _klass = POI
    
    def get_by_id(self, id):
        return self._klass.get_by_id(int(id))
    
    def search(self, word, page=1, query_id = None):
        q = self._klass.all().search(word).order('-modified')
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_id_user(self, id, user):
        if not isinstance(user, User):
            raise TypeError()
        poi = self._klass.get_by_id(int(id))
        if poi is None:
            return None
        if poi.user.key() != user.key():
            raise ForbiddenAccess()
        return poi
    
class PrivatePlaceHelper(POIHelper):
    _klass = PrivatePlace
    
    def get_by_business_user(self, business, user, page=1, query_id=None):
        if not isinstance(business, Business):
            raise TypeError()
        q = self._klass.gql('WHERE business = :1 AND user = :2', business, user)
        p = PagedQuery(q, id = query_id)
        return [p.id, p.fetch_page(page)]
    
    def get_by_address_or_point_user(self, address, user, point = None):
        if address != '' or address is not None:
            return self._klass.gql('WHERE address = :1 AND user = :2', address, user).get()
        return self._klass.gql('WHERE point = :1 AND user = :2', point, user).get()
    
class PlaceHelper(POIHelper):
    pass
    
