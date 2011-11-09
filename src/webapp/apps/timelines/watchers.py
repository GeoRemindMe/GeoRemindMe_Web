# coding=utf-8

import logging
logger = logging.getLogger(__name__)

from userena.signals import signup_complete

from models import Timeline
from funcs import DEBUG

def new_user_registered(sender, **kwargs):
    """
    Captura la señal de un nuevo usuario registrado,
    escribe el primer timeline
    """
    user = kwargs['user']
    Timeline.objects.add_timeline(user = user,
                                      msg_id = 0,
                                      instance = user,
                                      visible = False)
    DEBUG('TIMELINE: creado nuevo usuario %s' % user)
signup_complete.connect(new_user_registered)