# coding=utf-8

"""
.. module:: models
    :platform: appengine
    :synopsis: Modelo de _Report_Bug
"""


from google.appengine.ext import db
from geouser.models import User


class _Report_Bug(db.Model):
    """Almacena los bugs recibidos desde el movil"""
    user = db.ReferenceProperty(User, required=False)
    datetime = db.DateTimeProperty()
    msg = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)