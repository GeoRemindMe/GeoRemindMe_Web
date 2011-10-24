# coding=utf-8

"""
.. module:: signals
    :platform: appengine
    :synopsis: Observadores de señales de geouser
"""

import logging

from signals import user_new, user_social_new, user_follower_new, user_following_deleted, user_timeline_new


def new_user_registered(sender, **kwargs):
    """
        Captura la señal de un nuevo usuario registrado,
        escribe el primer timeline
    """
    if kwargs['status'] is None:
        logging.error('Problema registrando usuario %s') % sender.email
        sender.delete()
        from exceptions import RegistrationException
        raise RegistrationException()
    sender.send_confirm_code()
    from models_acc import UserTimelineSystem
    timeline = UserTimelineSystem(parent = sender, msg_id=0)
    logging.info('Registrado nuevo usuario %s email: %s' % (sender.id, sender.email))
    timeline.put()
user_new.connect(new_user_registered)


def new_social_user_registered(sender, **kwargs):
    """
        Captura la señal de un nuevo usuario de red social,
        escribe su timeline
    """
    from models_acc import UserTimelineSystem
    from models_social import GoogleUser, FacebookUser, TwitterUser
    if isinstance(sender, GoogleUser):
        timeline = UserTimelineSystem(parent = sender.user, msg_id=1)
        logging.info('Usuario con email %s ahora tiene cuenta de Google: %s' % (sender.user.email, sender.uid))
    elif isinstance(sender, FacebookUser):
        timeline = UserTimelineSystem(parent = sender.user, msg_id=2)
        logging.info('Usuario con email %s ahora tiene cuenta de Facebook: %s' % (sender.user.email, sender.uid))
    elif isinstance(sender, TwitterUser):
        timeline = UserTimelineSystem(parent = sender.user, msg_id=3)
        logging.info('Usuario con email %s ahora tiene cuenta de Twitter: %s' % (sender.user.email, sender.uid))
    else:
        return
    timeline.put()
user_social_new.connect(new_social_user_registered)


def new_follower(sender, **kwargs):
    """
        Captura la señal de un nuevo seguidor
        Escribe en el timeline de los dos usuarios.
        Envia una notificacion al correo.
        Escribe en el timeline de notificaciones
    """
    from google.appengine.ext import db
    from models_acc import UserTimelineSystem, UserTimeline, UserSettings
    if not isinstance(kwargs['following'], db.Key):
        raise AttributeError
    if kwargs['following'].id() == 962005 or sender.username == 'georemindme':
        return 
    from google.appengine.ext.deferred import defer
    defer(UserTimeline.add_timelines_to_follower, kwargs['following'], sender.key())
    settings = UserSettings.objects.get_by_id(kwargs['following'].id())
    timeline = UserTimelineSystem(parent = sender, instance = kwargs['following'], msg_id=100, visible=False)
    put = db.put_async([timeline])
    if settings.show_followings:
        timelinePublic = UserTimeline(user = sender, instance = kwargs['following'], msg_id=100)
        timelinePublic.put()
    from google.appengine.ext.deferred import defer
    defer(settings.notify_follower, sender.key())  # mandar email de notificacion
    put.get_result()
    if sender.key() != kwargs['following']:
        from geouser.models_utils import _Notification
        notification = _Notification(parent=kwargs['following'], timeline=timeline)
        notification.put()
user_follower_new.connect(new_follower)   


def deleted_following(sender, **kwargs):
    """
        Captura la señal indicando que se ha dejado
        de seguir a un usuario
        Escribe en el timeline del usuario
        En el caso de que no se enviara todavia la notificacion
        al mail, se borra el mensaje de un nuevo seguidor.
    """
    from models_acc import UserTimelineBase
    timelines = UserTimelineBase.all().filter('user =', sender).filter('msg_id =', 100).filter('instance =', kwargs['following']).run()
    from geouser.models_utils import _Report_Account_follower
    from google.appengine.ext.deferred import defer
    defer(_Report_Account_follower.insert_or_update, kwargs['following'], add=None, delete = sender.key())
    for timeline in timelines:
        timeline.delete()
user_following_deleted.connect(deleted_following)


def new_timeline(sender, **kwargs):
    """
        Captura la señal de un nuevo timeline
        Añade a la cola de tareas de notificaciones
    """
    if sender._is_public():
        from georemindme.tasks import NotificationHandler
        NotificationHandler().timeline_followers_notify(sender)
user_timeline_new.connect(new_timeline)
        
        


    
    
