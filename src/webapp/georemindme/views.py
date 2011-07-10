# coding=utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from cron import *
from tasks import *

def register_panel(request, login=False):
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    
    return render_to_response("webapp/register.html", {'login' :login}, context_instance=RequestContext(request))


def login_panel(request,login=False):
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    return render_to_response("webapp/login.html", {'login' :login}, context_instance=RequestContext(request))

def set_language(request):
    if request.method == 'POST':
        from django.conf import settings
        available = dict(settings.LANGUAGES)
        lang = request.POST.get('lang', settings.LANGUAGE_CODE)
        next = request.POST.get('next', '/')
        if lang in available: #we have the lang_code
            request.session['LANGUAGE_CODE'] = lang
        if request.session.get('user', None):
            settings = request.user.settings
            settings.language = lang
            settings.put()
        return HttpResponseRedirect(next)
        
    return HttpResponseRedirect(request.path)

