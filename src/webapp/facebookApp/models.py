# coding=utf-8

from google.appengine.ext import db

class _FacebookPost(db.Model):
    instance = db.StringProperty()
    post = db.StringProperty()