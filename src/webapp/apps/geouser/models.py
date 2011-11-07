# coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

TIME_CHOICES = (
           (0, _(u'Nunca')),
           (1, _(u'Inmediato')),
           (2, _(u'Diario')),
           (3, _(u'Semanal')),
           (4, _(u'Mensual')),
)

AVATAR_CHOICES = (
            (0, _(u'No utilizar')),
            (1, _(u'Gravatar')),
            (2, _(u'Facebook')),
            (3, _(u'Twitter')),
)
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    
    notification_invitation = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1, 
                                               verbose_name=_(u"Notificar invitaciones")
                                              )
    notification_suggestion = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1, 
                                               verbose_name=_(u"Notificar cambios tus sugerencias")
                                              )
    notification_account = models.PositiveSmallIntegerField(choices=TIME_CHOICES,
                                               default=1, 
                                               verbose_name=_(u"Notificar cuando te siguen")
                                              )
    show_followers = models.BooleanField(default=True, 
                                         verbose_name=_(u"Mostrar quien te sigue")
                                         )
    show_followers = models.BooleanField(default=True, 
                                         verbose_name=_(u"Mostrar a quien sigues")
                                         )
    
    avatar = models.URLField(blank=True)
    sync_avatar_with = models.IntegerField
    sync_avatar_with = models.PositiveSmallIntegerField(choices = AVATAR_CHOICES,
                                                        default=1,
                                                        verbose_name=_(u'Sincronizar tu avatar con')
                                        )
    
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)
    
