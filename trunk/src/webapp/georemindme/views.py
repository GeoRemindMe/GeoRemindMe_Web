# coding: utf-8
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
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import NotSavedError

from decorators import login_required
from models import User, GeoUser, GoogleUser, Alert, Point
from forms import *
from funcs import getAlertsJSON

"""
    logout function
    
    
"""    
def logout(request):
    request.session.delete()
    
    #return HttpResponseRedirect(users.create_logout_url(reverse('georemindme.views.home')))
    #return HttpResponseRedirect(users.create_logout_url("/"))
    return HttpResponseRedirect("/")

@login_required
def dashboard(request):

    alerts = Alert.objects.get_by_user(request.session['user'])

    return render_to_response("webapp/dashboard.html", dict(alerts=alerts), context_instance=RequestContext(request))

def home(request, login=False):  
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('georemindme.views.dashboard'))
    
    #return render_to_response("webapp/home.html", dict(login=login),context_instance=RequestContext(request))
    return render_to_response("webapp/home.html", dict(login=login), context_instance=RequestContext(request))

def private_home(request, login=False):
    
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('georemindme.views.dashboard'))
    
    #return render_to_response("webapp/home.html", dict(login=login),context_instance=RequestContext(request))
    return render_to_response("webapp/home_private_beta.html", dict(login=login), context_instance=RequestContext(request))


def set_language(request):
    if request.method == 'POST':
        from django.conf import settings
        available = dict(settings.LANGUAGES)
        lang = request.POST.get('lang', settings.LANGUAGE_CODE)
        next = request.POST.get('next', '/')
        if lang in available: #we have the lang_code
            request.session['LANGUAGE_CODE'] = lang
        return HttpResponseRedirect(next)
        
    return HttpResponseRedirect(reverse('georemindme.home'))

def confirm(request, user, code):
    u = User.objects.get_by_email_not_confirm(user)
    if u is not None:
        if u.confirm_code == code:
            u.toggle_confirmed()
            u.put()
            msg = _("User %s confirmed. Please log in.") % user
            return render_to_response('webapp/confirmation.html', dict(msg=msg), context_instance=RequestContext(request))
    msg = _("Invalid user %s") % user
    return render_to_response('webapp/confirmation.html', dict(msg=msg), context_instance=RequestContext(request))

def demo(request):
    
    from funcs import init_user_session
    
    
    u = User.objects.get_by_email("raubn.one@gmail.com")


    if u:
        init_user_session(request, u, remember=False)

    return HttpResponseRedirect(reverse("georemindme.views.dashboard"))


def json(request):
    return render_to_response('json.html')



