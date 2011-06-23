from google.appengine.ext import db
from georemindme.models_indexes import Invitation

class ListFollowersIndex(db.Model):
    followers = db.ListProperty(db.Key)
    count = db.IntegerProperty(default=0)
    _kind = db.TextProperty()