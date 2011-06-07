# coding=utf-8
from google.appengine.ext import db
from geouser.models import *


""" QUIZAS SERIA MEJOR LLEVAR LAS INVITACIONES ACEPTADAS COMO UNA LISTA Y NO CREAR UNA NUEVA INSTANCIA POR CADA LISTA
class InvitacionAceptadaIndex(db.Model):
    recomendacion = db.ReferenceProperty(Recomendacion)
    users = db.ListProperty(db.Key)
""" 

class InvitationHelper(object):
    
    def get_user_invited(self, instance, user):
        if getattr(instance, 'user', None) == user:
            return True
        invitation = db.GqlQuery('SELECT __KEY__ FROM Invitation WHERE instance = :ins AND to = :user', ins=instance.key(), user=user.key()).get()
        if invitation is not None:
            return True
        return False
    

class Invitation(db.Model):
    """Por cada invitacion, se crea una nueva instancia"""
    sender = db.ReferenceProperty(User, collection_name='senderinvitation_set')
    to = db.ReferenceProperty(User, collection_name='toinvitation_set')
    created = db.DateTimeProperty(auto_now_add=True)
    instance = db.ReferenceProperty(None, required = True)
    status = db.IntegerProperty(default=0)
    
    objects = InvitationHelper()