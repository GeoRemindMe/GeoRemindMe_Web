# coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class UserFollowingUser(models.Model):
    follower = models.ForeignKey(User, 
                                 blank=False,
                                 verbose_name=_(u"Seguidor"),
                                 related_name='followees'
                                 )
    followee = models.ForeignKey(User, 
                                 blank=False,
                                 verbose_name=_(u"Seguido"),
                                 related_name='followers'
                                 )
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("follower", "followee"),)
        
        
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
                             verbose_name=_(u"Dueño")
                             )
    msg_id = models.PositiveSmallIntegerField(blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('content_type', 'object_id') # clave generica para cualquier modelo    
    visible = models.BooleanField(default=True,
                                  verbose_name=_(u"Visibilidad del timeline"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    

class TimelineFollowers(models.Model):
    timeline = models.ForeignKey(Timeline,
                                 blank=False)
    follower = models.ForeignKey(User,
                                 blank=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "created"
        ordering = ['-created']
        unique_together = (("timeline", "follower"),)