# coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaLanguageBaseProfile
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from modules.timezones.fields import TimeZoneField

#from south.modelsinspector import add_introspection_rules
#add_introspection_rules([], ["^modules.timezones.fields.TimeZoneField"])

class UserProfile(UserenaLanguageBaseProfile):
    AVATAR_CHOICES = (
                (0, _(u'No utilizar')),
                (1, _(u'Gravatar')),
                (2, _(u'Facebook')),
                (3, _(u'Twitter')),
    )
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('usuario'),
                                related_name='profile')
    
    show_followers = models.BooleanField(_("Mostrar quien te sigue"),
                                         default=True, 
                                         )
    show_followings = models.BooleanField(_("Mostrar a quien sigues"),
                                         default=True, 
                                         )
    counter_suggested = models.PositiveIntegerField(_("Contador de sugerencias creadas"),
                                                    default=0,
                                                    )
    counter_followers = models.PositiveIntegerField(_("Contador de seguidores"),
                                                    default=0,
                                                    )
    counter_followings = models.PositiveIntegerField(_("Contador de seguidos"),
                                                     default=0,
                                                     )
    counter_notifications = models.PositiveIntegerField(_("Contador de notificaciones pendientes"),
                                                        default=0,
                                                        )
    counter_supported = models.PositiveIntegerField(_("Contador de notificaciones pendientes"),
                                                    default=0,
                                                    )
    
    class Meta:
        verbose_name = _('Perfil de usuario')
        verbose_name_plural = _('Perfiles de usuario')
    
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)


