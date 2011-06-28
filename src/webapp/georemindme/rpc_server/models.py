# coding=utf-8

from google.appengine.ext import db

class _Report_Bug(db.Model):
    user = db.ReferenceProperty(User, required=False)
    datetime = db.DateTimeProperty()
    msg = db.TextProperty()