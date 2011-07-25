# coding=utf-8

from django.utils.translation import gettext_lazy as _

from google.appengine.ext import db
from geouser.models import User

class _Report_Bug(db.Model):
    user = db.ReferenceProperty(User, required=False)
    datetime = db.DateTimeProperty()
    msg = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)