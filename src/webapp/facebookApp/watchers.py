# coding=utf-8
from google.appengine.ext import db

from geouser.signals import *
from geoauth.clients.facebook import *

def new_follower_notification(sender, **kwargs):
    '''
    Sender empieza a seguir a un nuevo usuario
    sender= es quien envía la señal objeto tipo User
    kwargs['following'] = objetivo user al que empiezan a seguir
    
    '''
    user_followed=db.get(kwargs['following'])
    fb_client=FacebookClient(user=kwargs['following'])
    #~ raise Exception(fb_client.consumer.access_token)
    params= {
        "name": "Link name",
        "link": "http://www.example.com/",
        "caption": "{*actor*} posted a new review",
        "description": "This is a longer description of the attachment",
        "picture": "http://www.example.com/thumbnail.jpg",
        "privacy": {'value':'CUSTOM','friends':'SELF'}
    }
    fb_client.consumer.put_wall_post("%(id)s (%(username)s) ha empezado a seguirte" % {'id':sender.id, 'username':sender.username}, params);
    #~ friends_to_follow=fb_client.get_friends_to_follow()
    
    #~ raise Exception(user_followed.facebook_user.uid)
    
user_follower_new.connect(new_follower_notification)   
