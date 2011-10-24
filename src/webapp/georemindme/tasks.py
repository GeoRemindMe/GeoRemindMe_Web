# coding=utf-8

import os
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api import mail

from geouser.models import User
from geouser.models_acc import UserTimeline, UserTimelineBase


def admin_required(func):
    def _wrapper(*args, **kwargs):
        if 'HTTP_X_APPENGINE_TASKNAME' in os.environ:
            return func(*args, **kwargs)
        session = args[0].session
        user = session.get('user')
        if user and user.is_admin():
            return func(*args, **kwargs)
        return HttpResponseForbidden()
    return _wrapper


class TaskHandler(object):
    def add(self):
        pass
    
#===============================================================================
# ENVIO DE EMAILS
#===============================================================================
class EmailHandler(TaskHandler):
    '''
    Clase encargada de gestionar la cola de envio de correos
    '''
    def add(self, email):
        taskqueue.add(url='/tasks/email/', 
                      params = { 'sender': email.sender,
                                                   'to': email.to,
                                                   'subject': email.subject,
                                                   'body' : email.body,
                                                   'html': email.html if hasattr(email, 'html') else None,
                                                   },
                      method = 'POST',
                      queue_name="email")


@csrf_exempt
@admin_required
def email_worker(request):
    mail.send_mail(sender=request.POST['sender'], 
                   to=request.POST['to'], 
                   subject=request.POST['subject'], 
                   body=request.POST['body'], 
                   html=request.POST['html'])
    return HttpResponse()

#===============================================================================
# NOTIFICACIONES A FOLLOWERS
#===============================================================================
class NotificationHandler(TaskHandler):
    def timeline_followers_notify(self, timeline):
        taskqueue.add(url='/tasks/notify/timeline/',
                      params = { 'timeline': timeline.key() },
                      method = 'POST',
                      queue_name='timelineFollowers')
        
    def list_followers_notify(self, list):
        '''
        Notifica a los seguidores de la lista que esta se modifico
        '''
        taskqueue.add(url='/tasks/notify/list/',
                      params = {'list': list.key()},
                      method = 'POST',
                      queue_name='listFollowers')
    
@csrf_exempt
@admin_required
def timelinefollowers_worker(request):
    timeline = db.get(request.POST['timeline'])
    if timeline is not None:
        if not hasattr(timeline, 'notify_followers'):
            return HttpResponse()
        notified = timeline.notify_followers()
        if notified:
            return HttpResponse()
    return HttpResponse()

@csrf_exempt
@admin_required
def list_notify_worker(request):
    list = db.get(request.POST['list'])
    if list is not None:
        if not hasattr(list, 'notify_followers'):
            return HttpResponse()
        notified = list.notify_followers()
        if notified:
            return HttpResponse()
    return HttpResponse()
    
        
        
    
