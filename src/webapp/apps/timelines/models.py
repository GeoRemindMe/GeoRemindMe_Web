# coding=utf-8


from django.db import models, connection
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from signals import timeline_added, follower_added, follower_deleted
from funcs import BatchInsertQuery


class NotificationSettings(models.Model):
    TIME_CHOICES = (
           (0, _(u'Nunca')),
           (1, _(u'Inmediato')),
           (2, _(u'Diario')),
           (3, _(u'Semanal')),
           (4, _(u'Mensual')),
    )
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('usuario'),
                                related_name='notification_settings')
    
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

    class Meta:
        verbose_name = _('Configuracion de notificaciones')
        verbose_name_plural = _('Configuraciones de notificaciones')
   

#------------------------------------------------------------------------------ 
class FollowerManager(models.Manager):
    def is_follower(self, follower, followee, **kwargs):
        follower_type = ContentType.objects.get_for_model(type(follower))
        followee_type = ContentType.objects.get_for_model(type(followee))
        
        return self.filter(follower_id=follower.id,  
                        follower_c_type=follower_type,
                        followee_id=followee.id, 
                        followee_c_type=followee_type).exists()
        
    def toggle_follower(self, follower, followee, **kwargs):
        follower_type = ContentType.objects.get_for_model(type(follower))
        followee_type = ContentType.objects.get_for_model(type(followee))
        
        q = self.filter(follower_id=follower.id, follower_c_type=follower_type,
                                  followee_id=followee.id, followee_c_type=followee_type)
        
        if q.exists():
            self.q.delete()
            follower_deleted.send(follower=follower, followee=followee)
        else:
            self.create(follower=follower, followee=followee, **kwargs)
            follower_added.send(follower=follower, followee=followee)
    
    def get_by_follower(self, follower, type_filter=None):
        follower_type = ContentType.objects.get_for_model(type(follower))
        if type_filter is not None:
            followee_type = ContentType.objects.get_for_model(type(type_filter))
            return self.filter(follower_id=follower.id, 
                                follower_c_type=follower_type,
                                followee_c_type=followee_type).select_related(depth=1)
        else:
            return self.filter(follower_id=follower.id, 
                                follower_c_type=follower_type).select_related(depth=1)
                                
    def get_by_followee(self, followee, type_filter=None):
        followee_type = ContentType.objects.get_for_model(type(followee))
        if type_filter is not None:
            followee_type = ContentType.objects.get_for_model(type(type_filter))
            return self.filter(follower_id=followee.id, 
                                follower_c_type=followee_type,
                                followee_c_type=followee_type).select_related(depth=1)
        else:
            return self.filter(followee_id=followee.id,
                               followee_c_type=followee_type).select_related(depth=1)

class Follower(models.Model):
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _("Tipo de objeto seguidor"),
                                        related_name = "followings")
    follower_id = models.PositiveIntegerField(_("Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo

    followee_c_type = models.ForeignKey(ContentType,
                                     verbose_name = _("Tipo de objeto seguido"),
                                     related_name = "followers")
    followee_id = models.PositiveIntegerField(_("Identificador del seguido"))
    followee = generic.GenericForeignKey('followee_c_type', 'followee_id',) # clave generica para cualquier modelo
    
    created = models.DateTimeField(auto_now_add=True)
    objects = FollowerManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("follower_c_type", "follower_id", "followee_c_type", "followee_id"),)
        verbose_name = _('Seguimiento')
        verbose_name_plural = _('Seguimientos')


#------------------------------------------------------------------------------ 
class TimelineManager(models.Manager):
    def add_timeline(self, user, msg_id, instance, visible, **kwargs):
        timeline = self.create(user = user,
                    msg_id = msg_id,
                    instance = instance,
                    visible = visible,
                    **kwargs)
        timeline_added.send(timeline)
        
    
    def get_by_instance(self, instance, visible=True):
        """
            Obtiene el timeline publico perteneciente a un objeto
            
            :param instance: objeto a buscar
            :type instance: Cualquiera
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
            :returns: Iterator
            
        """
        c_type = ContentType.objects.get_for_model(type(instance))
        return self.filter(instance_id=object.id, content_type=c_type, visible=visible)#.iterator()
    
    def get_by_user(self, user, visible=True):
        """
            Obtiene el timeline publico o privado de un usuario
            
            :param user: Usuario a buscar
            :type user: :class:`django.contrib.auth.User`
            :param visible: Solo si el timeline es publico o todo
            :type visible: :class:`Boolean`
            
        """
        return self.filter(user=user, visible=True)#.iterator()


class Timeline(models.Model):
    ## 0: _('Welcome to GeoRemindMe you can share your public profile: \
    ## <a href="http://www.georemindme.com/user/%(username)s/">\
    ## http://www.georemindme.com/user/%(username)s/</a>') %{
    ## 'username':self.user.username,
    ## },
    ## 1: _('Now, you can log with your Google account'),
    ## 2: _('Now, you can log from Facebook and from <a href="http://www.georemindme.com" target="_blank">www.georemindme.com</a>'),
    ## 3: _('Now, you can log with your Twitter account'),
    ##
    ## #User messages
    ## 100: _('You are now following <a href="%(profile_url)s">%(username)s</a>') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 101: _('<a href="%(profile_url)s">%(username)s</a> is now following you') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 102: _('You are no longer following <a href="%(profile_url)s">%(username)s</a> anymore') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.instance
    ## },
    ## 110: _('You invited %s to:') % self.instance,
    ## 111: _('%s invited you to %s') % (self.instance, self.instance),
    ## 112: _('%s accepted your invitation to %s') % (self.user, self.instance),
    ## 113: _('%s rejected your invitation to %s') % (self.user, self.instance),
    ## 120: _('<a href="%(profile_url)s">%(username)s</a> ha hecho un comentario en la sugerencia: <br><a href="/fb/suggestion/%(suggestion_id)s/">%(suggestion)s</a>') % {
    ## 'profile_url':self.user.get_absolute_url(),
    ## 'username':self.user,
    ## 'suggestion':self.instance,
    ## 'suggestion_id':self.instance,
    ## },
    ## 125: _('likes a comment: %s') % self.instance,
    ## 150: _('New user list created: %s') % self.instance,
    ## 151: _('User list modified: %s') % self.instance,
    ## 152: _('User list removed: %s') % self.instance,
    ##
    ## #Alerts
    ## 200: _('New alert: %s') % self.instance,
    ## 201: _('Alert modified: %s') % self.instance,
    ## 202: _('Alert deleted: %s') % self.instance,
    ## 203: _('Alert done: %s') % self.instance,
    ##
    ## #Alerts lists
    ## 250: _('New alert list created: %s') % self.instance,
    ## 251: _('Alert list modified: %s') % self.instance,
    ## 252: _('Alert list removed: %s') % self.instance,
    ##
    ## #Suggestions
    ## 300: _('<a href="/fb%(url)s">%(username)s</a> sugiere:<br> %(message)s') % {
    ## 'url':self.user.get_absolute_url(),
    ## 'username':self.user.username,
    ## 'message':self.instance
    ## },
    ## 301: _('Suggestion modified: %s') % self.instance,
    ## 302: _('Suggestion removed: %s') % self.instance,
    ## 303: _('You are following: %s') % self.instance,
    ## 304: _('You stopped following: %s') % self.instance,
    ## 305: _('likes a suggestions: %s') % self.instance,
    ## 320: _('New alert: %s') % self.instance,
    ## 321: _('Alert modified: %s') % self.instance,
    ## 322: _('Alert deleted: %s') % self.instance,
    ## 323: _('Alert done: %s') % self.instance,
    ##
    ## #Suggestions list
    ## 350: _('New suggestions list created: %s') % self.instance,
    ## 351: _('Suggestions list modified: %s') % self.instance,
    ## 352: _('Suggestion list removed: %s') % self.instance,
    ## 353: _('You are following: %s') % self.instance,
    ## 354: _('You are not following %s anymore') % self.instance,
    ##
    ## #Places
    ## 400: _('New private place: %s') % self.instance,
    ## 401: _('Private place modified: %s') % self.instance,
    ## 402: _('Private place deleted: %s') % self.instance,
    ## 450: _('New public place: %s') % self.instance,
    ## 451: _('Public place modified: %s') % self.instance,
    ## 452: _('Public place deleted: %s') % self.instance,
    ##
    user = models.ForeignKey(User,
                             blank=False,
                             verbose_name=_("Usuario")
                             )
    msg_id = models.PositiveSmallIntegerField(_("Tipo de mensaje"))
    content_type = models.ForeignKey(ContentType,
                                     verbose_name = _("Tipo de instancia"))
    object_id = models.PositiveIntegerField(_("Identificador de instancia"))
    instance = generic.GenericForeignKey('content_type', 'object_id') # clave generica para cualquier modelo    
    visible = models.BooleanField(_("Visible en perfil publico"),
                                  default=True,
                                  )
    created = models.DateTimeField(_("Creado"),
                                   auto_now_add=True)
    modified = models.DateTimeField(_("Modificado"),
                                      auto_now=True)
    
    objects = TimelineManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        verbose_name = _('Timeline')
        verbose_name_plural = _('Timelines')
        
    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return "%s - %d - %s" % (self.user, self.id, self.modified)
    
    def delete(self, *args, **kwargs):
        TimelineFollower.objects.filter(timeline_id=self.id).delete()
        super(self.__class__, self).delete()
        

#------------------------------------------------------------------------------ 
class TimelineFollowerManager(models.Manager):
    def batch_insert( self, *instances ):
        """
        Issues a batch INSERT using the specified model instances.
        """
        cls = instances[0].__class__
        query = BatchInsertQuery( cls, connection)
        for instance in instances:
            values = [ (f, f.get_db_prep_save( f.pre_save( instance, True ) ) ) \
                 for f in cls._meta.local_fields ]
            query.insert_values( values )

        return query.execute_sql()


class TimelineFollower(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 blank=False)
    
    follower_c_type = models.ForeignKey(ContentType,
                                        verbose_name = _("Tipo de objeto seguidor"),
                                        related_name = "timelinefollowings")
    follower_id = models.PositiveIntegerField(_("Identificador del seguidor"))
    follower = generic.GenericForeignKey('follower_c_type', 'follower_id',) # clave generica para cualquier modelo
    
    created = models.DateTimeField(auto_now_add=True)
    objects = TimelineFollowerManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("timeline", "follower_c_type", "follower_id"),)
        verbose_name = _('Notificacion de Timeline')
        verbose_name_plural = _('Notificaciones de Timelines')
        
    def __unicode__(self):
        return "%s - %s - %d" % (self.follower, self.timeline, self.created)