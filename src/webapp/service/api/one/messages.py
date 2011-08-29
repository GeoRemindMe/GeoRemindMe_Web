# coding=utf-8


from protorpc import messages


class Timeline(messages.Message):
    msg = messages.StringField(1)
    instance_id = messages.IntegerField(2)
    instance_name = messages.StringField(3)
    user = messages.StringField(4)
    created = messages.IntegerField(5)
    

class Timelines(messages.Message):
    timelines = messages.MessageField(Timeline, 1, repeated=True)
    
    
class Suggestion(messages.Message):
    name = messages.StringField(1, required=True)
    description = messages.StringField(2)
    poi_lat = messages.FloatField(3)
    poi_lon = messages.FloatField(4)
    poi_id = messages.IntegerField(5)
    places_reference = messages.StringField(6)
    created = messages.IntegerField(7)
    modified = messages.IntegerField(8)
    client_id = messages.StringField(9)
    id = messages.IntegerField(10)
    lists = messages.IntegerField(11, repeated=True)
    

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
    
    

