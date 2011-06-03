# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see < http: // www.gnu.org / licenses /> .

"""
from datetime import timedelta, datetime
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from google.appengine.api import users
from funcs import getAlertsJSON, init_user_session, login_func
from georemindme.decorators import login_required, ajax_request
from georemindme.forms import *
from georemindme.models import User, GeoUser, GoogleUser
from django.utils import simplejson

@ajax_request
def exists(request):
    
    if not request.POST.get('email'):
        return HttpResponseBadRequest()

    user = User.objects.get_by_email( request.POST.get('email') )

    if user:
        return HttpResponse('{"result":"exists"}',mimetype="application/json")
    else:
        return HttpResponse('{"result":""}',mimetype="application/json")

@ajax_request
def register(request):
    f = RegisterForm(request.POST, prefix='user_register')
    data = {}
    if f.is_valid():
        user = f.save()
        if user:
            messages.success(request, _("User registration complete, a confirmation email have been sent to %s. Redirecting to dashboard...") % user.email)
            init_user_session(request, user)
            data['_redirect'] = reverse('georemindme.views.dashboard')
            return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    data['errors'] = f.errors
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

@ajax_request
def contact(request):
    
    from georemindme.mails import send_contact_email
    send_contact_email(request.POST.get('userEmail',''),request.POST.get('msg',''))
    
    return HttpResponse('')

@ajax_request
def keepuptodate(request):
    
    from georemindme.mails import send_keepuptodate
    
    data = ''
    for k in request.POST.keys():
        if k.endswith("version"):
            data+=(k+"<br/>")

    send_keepuptodate(request.POST.get('user-email',''),data)
    
    return HttpResponse('')


@ajax_request
@never_cache
def login(request):
    f = LoginForm(request.POST, prefix='user_login')    
    error = ''
    redirect = ''
    if f.is_valid():
        error, redirect = login_func(request, f)
    else:
        error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
    return HttpResponse(simplejson.dumps(dict(error=error, _redirect=redirect)), mimetype="application/json")


@ajax_request
@login_required
def add_reminder(request):
    
    form = RemindForm(request.POST)
    if form.is_valid():
        
        id = request.POST.get('id')
        
        if id:
            new = form.save(user=request.session['user'], address=request.POST['address'],id=int(id))
        else:
            new = form.save(user=request.session['user'], address=request.POST['address'])
            
        return HttpResponse(simplejson.dumps(dict(id=new.id)), mimetype="application/json")
    else:
        return HttpResponseBadRequest(simplejson.dumps(form.errors), mimetype="application/json")

@ajax_request
@login_required
def edit_reminder(request):
    form = RemindForm(request.POST)
    if form.is_valid():
        alert = form.save(id=request.POST.get('id'), user=request.session['user'], address=request.POST['address'])
        
        if alert is None:
            return HttpResponseBadRequest()
        else:
            return HttpResponse()
    else:
        return HttpResponseBadRequest(form.errors, mimetype="application/json")
        
@ajax_request
@login_required
def get_reminder(request):
    id = request.POST.get('id', None)
    done = request.POST.get('done', None)
    if id:
        alerts = [ Alert.objects.get_by_id_user(id, request.session['user']) ]
    else:
        if not done:
            alerts = Alert.objects.get_by_user(request.session['user'])
        elif done.lower() == 'true':
            alerts = Alert.objects.get_by_user_done(request.session['user'])
        else:
            alerts = Alert.objects.get_by_user_undone(request.session['user'])
    if len(alerts) == 0:
            return HttpResponse('[]', mimetype="application/json")
            #return HttpResponseBadRequest('Doesnt exist the alert or forbidden', mimetype="application/json")
    print getAlertsJSON(alerts)
    return HttpResponse(getAlertsJSON(alerts), mimetype="application/json")

@ajax_request
@login_required
def delete_reminder(request):
    id = request.POST.get('id')
    if not id:
        return HttpResponseBadRequest("No key provided", mimetype="text/plain")
    
    alert = Alert.objects.get_by_id_user(int(id), request.session['user'])
    
    if not alert:
            return HttpResponseBadRequest('Doesnt exist the alert or forbidden', mimetype="text/plain")
    alert.delete()    
    return HttpResponse()

