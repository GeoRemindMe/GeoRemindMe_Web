# coding=utf-8


from google.appengine.ext import db

from geouser.models import User

class User_c2dm(db.Model):
    user = db.ReferenceProperty(User)