from google.appengine.ext import db

from georemindme.models_indexes import Invitation
    
class SuggestionFollowersIndex(db.Model):
    keys = db.ListProperty(db.Key)
    count = db.IntegerProperty(default = 0)