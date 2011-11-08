# coding=utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

def home(request, login=False):
    if request.user.is_authenticated():
            return HttpResponseRedirect(request.user.get_absolute_url())
    return render_to_response("mainApp/home.html", 
                              {'login' : login}, 
                              context_instance=RequestContext(request)
                              )
    