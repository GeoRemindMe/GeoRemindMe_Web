# coding=utf-8

"""
.. module:: views
    :platform: appengine
    :synopsis: Vistas basicas para todo el proyecto
"""


from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from tasks import list_notify_worker, timelinefollowers_worker, email_worker
from cron import report_notify, clean_sessions
from geouser.decorators import username_required


def register_panel(request, login=False):
    if request.session.get('user'):
        return HttpResponseRedirect(reverse('geouser.views.dashboard'))
    return render_to_response("generic/register.html", {'login' :login}, context_instance=RequestContext(request))


def login_panel(request,login=False):
    try:
    # When deployed
        from google.appengine.runtime import DeadlineExceededError
    except ImportError:
    # In the development server
        from google.appengine.runtime.apiproxy_errors import DeadlineExceededError 
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('geouser.views.dashboard'))
        return render_to_response("mainApp/login.html", {'login' :login}, context_instance=RequestContext(request))
    except DeadlineExceededError:
        return HttpResponseRedirect('/')


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


@username_required
def search_suggestions(request, term=None, template='generic/search.html'):
    #from geoalert.forms import SuggestionForm
    #s = Suggestion.objects.get_by_id(suggestion_id)
    if not request.user.is_authenticated():
            pos = template.rfind('.html')
            template = template[:pos] + '_anonymous' + template[pos:]
    return  render_to_response(template, {'term': term,
                                          }, context_instance=RequestContext(request))
