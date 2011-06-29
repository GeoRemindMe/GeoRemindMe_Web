# coding=utf-8

from geouser.signals import *

def new_follower_notification(sender, **kwargs):
    '''
    Sender empieza a seguir a un nuevo usuario
    sender= es quien envía la señal objeto tipo User
    kwargs['following'] = objetivo user al que empiezan a seguir
    
    '''
    raise Exception(kwargs['following'].id)
    
user_follower_new.connect(new_follower_notification)   
