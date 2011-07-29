# coding=utf-8

"""
.. module:: models_indexes
    :platform: appengine
    :synopsis: Modelos para almacenar indices comunes a todo el proyecto
"""


from google.appengine.ext import db
from django.utils.translation import gettext_lazy as _

from geouser.models import User


""" QUIZAS SERIA MEJOR LLEVAR LAS INVITACIONES ACEPTADAS COMO UNA LISTA Y NO CREAR UNA NUEVA INSTANCIA POR CADA LISTA
class InvitacionAceptadaIndex(db.Model):
    recomendacion = db.ReferenceProperty(Recomendacion)
    users = db.ListProperty(db.Key)
""" 
class InvitationHelper(object):
    """ Helper de la clase Invitation """
    def is_user_invited(self, instance, user):
        """
        Comprueba si un usuario esta invitado a una instancia
        
            :param instance: instancia a la que deberia estar invitado
            :type instance: :class:`object`
            :param user: usuario que deberia estar invitado
            :type user: :class:`geouser.models.User`
            
            :returns: True si esta invitado, False en caso contrario
        """
        if getattr(instance, 'user', None) == user:
            return True
        invitation = db.GqlQuery('SELECT __key__ FROM Invitation WHERE instance = :ins AND to = :user', ins=instance.key(), user=user.key()).get()
        if invitation is not None:
            return True
        return False
    
    def get_invitation(self, instance, user):
        """
        Obtiene la invitacion (si existe) de un usuario a una instancia
        
            :param instance: instancia a la que deberia estar invitado
            :type instance: :class:`object`
            :param user: usuarios que deberia tener la invitacion
            :type user: :class:`geouser.models.User`
            
            :returns: :class:`georemindme.model_indexes.Invitation` o None
        """
        if getattr(instance, 'user', None) == user:
            return True
        invitation = Invitation.all().filter('instance =', instance).filter('to =', user).get()
        return invitation
    

class Invitation(db.Model):
    """Por cada invitacion, se crea una nueva instancia"""
    sender = db.ReferenceProperty(User, collection_name='senderinvitation_set')
    to = db.ReferenceProperty(User, collection_name='toinvitation_set')
    created = db.DateTimeProperty(auto_now_add=True)
    instance = db.ReferenceProperty(None, required = True)
    """
    STATUS CODES:
            0 - Pending
            1 - Accepted
            2 - Declined
            3 - Ignored
    """
    status = db.IntegerProperty(default=0)
    objects = InvitationHelper()
    
    @classmethod
    def send_invitation(cls, sender, to, instance, status=0):
        """
        Envia una invitacion a un usuario. Si la instancia es algun objeto privado, 
        lanza excepcion.
        
            :param sender: usuario que envia la invitacion
            :type sender: :class:`geouser.models.User`
            :param to: usuario que recibe la invitation
            :type to: :class:`geouser.models.User`
            :param status: estado iniciail de la invitacion (0 por defecto)
            :type status: :class:`integer`
            
            :returns: :class:`georemindme.models_indexes.Invitation`
            :raises: :class:`georemindme.exceptions.PrivateException` si el objeto es privado
        """
        invitation = cls.objects.get_invitation(instance, to)
        if invitation is not None:
            if invitation.status == 2:  # la invitacion fue rechazada, se creara otra
                #  TODO: habria que evitar que pudiera haber spam de invitaciones
                invitation.delete()
            else:
                return invitation
        invitation = Invitation(sender=sender, to=to, instance=instance, status=status)
        invitation.put()
        return invitation
    
    def accept(self):
        self.status = 1
        self.put()
        
    def decline(self):
        self.status = 2
        self.put()
        
    def ignore(self):
        self.status = 3
        self.put()
        
    def set_status(self, set_status=0):
        self.status = set_status
        self.put()
        from signals import invitation_changed
        invitation_changed.send(sender=self)
         
    def put(self):
        if not self.is_saved():
            super(Invitation, self).put()
            from geouser.models_acc import UserTimelineSystem
            timeline = UserTimelineSystem(user=self.sender, msg_id=110, instance=self)
            timeline2 = UserTimelineSystem(user=self.to, msg_id=111, instance=self)
            put = db.put_async([timeline, timeline2])            
            if self.to.settings.notification_invitation:
                from geomail import send_notification_invitation
                send_notification_invitation(self.to.email, self.sender, self)
            put.get_result()
        else:
            super(Invitation, self).put()            
