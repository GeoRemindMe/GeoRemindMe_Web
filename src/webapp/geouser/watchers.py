# coding=utf-8

import logging

from signals import *
from exceptions import *

from models_social import *
from models_acc import *

def new_user_registered(sender, **kwargs):
    '''
    Un nuevo usuario se registra, escribimos el primer timeline
    '''
    if kwargs['status'] is None:
        logging.error('Problema registrando usuario %s') % sender.email
        sender.delete()
        raise RegistrationException()
    sender.send_confirm_code()
    timeline = UserTimelineSystem(user = sender, msg_id=0)
    logging.info('Registrado nuevo usuario %s email: %s' % (sender.id, sender.email))
    timeline.put()
user_new.connect(new_user_registered)
    
def new_social_user_registered(sender, **kwargs):
    '''
    Se da de alta un usuario de una red social 
    '''
    if isinstance(sender, GoogleUser):
        timeline = UserTimelineSystem(user = sender.user, msg_id=1)
        logging.info('Usuario con email %s ahora tiene cuenta de Google: %s' % (sender.user.email, sender.uid))
    elif isinstance(sender, FacebookUser):
        timeline = UserTimelineSystem(user = sender.user, msg_id=2)
        logging.info('Usuario con email %s ahora tiene cuenta de Facebook: %s' % (sender.user.email, sender.uid))
    elif isinstance(sender, TwitterUser):
        timeline = UserTimelineSystem(user = sender.user, msg_id=3)
        logging.info('Usuario con email %s ahora tiene cuenta de Twitter: %s' % (sender.user.email, sender.uid))
    else:
        return
    timeline.put()
user_social_new.connect(new_social_user_registered)


def new_follower(sender, **kwargs):
    '''
    Sender empieza a seguir a un nuevo usuario
    '''
    timeline = UserTimelineSystem(user = sender, instance = kwargs['following'], msg_id=100)
    timelineFollowing = UserTimelineSystem(user=kwargs['following'], instance=sender, msg_id=101)
    put = db.put_async([timeline, timelineFollowing])
    settings = UserSettings.objects.get_by_id(kwargs['following'].id())
    settings.notify_follower(sender)  # mandar email de notificacion
    put.get_result()
user_follower_new.connect(new_follower)   

def deleted_following(sender, **kwargs):
    '''
    Sender deja de seguir a un nuevo usuario
    '''
    timeline = UserTimelineSystem(user = sender, instance = kwargs['following'], msg_id=102)
    timeline.put()
user_following_deleted.connect(deleted_following)

def new_timeline(sender, **kwargs):
    '''
    Sender ha escrito un nuevo timeline publico, notificar a los seguidores
    '''
    timeline = UserTimeline(user=sender, msg=kwargs['msg'],
                            instance=kwargs['instance'], _vis=kwargs['vis'])
    timeline.put()
user_timeline_new.connect(new_timeline)
        
        


    
    
