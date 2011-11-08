# coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaLanguageBaseProfile
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from modules.timezones.fields import TimeZoneField


class UserProfile(UserenaLanguageBaseProfile):
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
    # This field is required.
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u'Usuario'),
                                related_name='profile'
                                )
    timezone    = TimeZoneField(_(u"Timezone"))
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
    show_profile = models.BooleanField(default=True,
                                       verbose_name=_(u"Perfil publico")
                                       )
    avatar = models.URLField(blank=True)
    sync_avatar_with = models.IntegerField
    sync_avatar_with = models.PositiveSmallIntegerField(choices = AVATAR_CHOICES,
                                                        default=1,
                                                        verbose_name=_(u'Sincronizar tu avatar con')
                                        )
    counter_suggested = models.PositiveIntegerField(default=0,
                                              verbose_name=_(u"Contador de sugerencias creadas")
                                              )
    counter_followers = models.PositiveIntegerField(default=0,
                                              verbose_name=_(u"Contador de seguidores")
                                              )
    counter_followings = models.PositiveIntegerField(default=0,
                                              verbose_name=_(u"Contador de seguidos")
                                              )
    counter_notifications = models.PositiveIntegerField(default=0,
                                              verbose_name=_(u"Contador de notificaciones pendientes")
                                              )
    counter_supported = models.PositiveIntegerField(default=0,
                                              verbose_name=_(u"Contador de sugererencias votadas")
                                              )
    
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)
