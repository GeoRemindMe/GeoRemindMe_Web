# coding=utf-8


from protorpc import messages

    
class LoginResponse(messages.Message):
    session = messages.StringField(1)
    expires = messages.IntegerField(2)


class Timeline(messages.Message):
    msg = messages.StringField(1)
    msg_id = messages.IntegerField(2)
    instance_id = messages.IntegerField(3)
    instance_name = messages.StringField(4)
    url = messages.StringField(5)
    user = messages.StringField(6)
    created = messages.IntegerField(7)
    

class Timelines(messages.Message):
    timelines = messages.MessageField(Timeline, 1, repeated=True)
    query_id = messages.StringField(2)
    

class List(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    

class Comment(messages.Message):
    id = messages.IntegerField(1)
    username = messages.StringField(2)
    message = messages.StringField(3)
    created = messages.IntegerField(4)
    
    
class Suggestion(messages.Message):
    name = messages.StringField(1, required=True)
    description = messages.StringField(2)
    poi_lat = messages.FloatField(3)
    poi_lon = messages.FloatField(4)
    poi_id = messages.IntegerField(5)
    places_reference = messages.StringField(6)
    created = messages.IntegerField(7)
    modified = messages.IntegerField(8)
    username = messages.StringField(9)
    id = messages.IntegerField(10)
    lists = messages.MessageField(List, 11, repeated=True)
    comments = messages.MessageField(Comment, 13, repeated=True)
    has_voted = messages.BooleanField(14)
    vote_counter = messages.IntegerField(15)
    user_follower = messages.BooleanField(16)
    top_comments = messages.MessageField(Comment, 17, repeated=True)
    
    
    

class Suggestions(messages.Message):
    query_id = messages.StringField(1)
    suggestions = messages.MessageField(Suggestion, 2, repeated=True)
    

class Site(messages.Message):
    name = messages.StringField(1, required=True)
    address = messages.StringField(2)
    lat = messages.FloatField(3)
    lon = messages.FloatField(4)
    
    
class Sites(messages.Message):
    sites = messages.MessageField(Site, 1, repeated=True)
