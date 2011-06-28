# coding=utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from models import *
from django.template import RequestContext

from settings import OAUTH, FACEBOOK_APP

def setupVars(request):
    initialization=BaseHandler(request, None)
    
    print initialization.facebook
    

#~ @csrf_exempt
def login_panel(request):
    #~ setupVars(request)
    if BaseHandler.user:
        return  render_to_response('welcome.html',{'data':data,'user':BaseHandler.user}, context_instance=RequestContext(request))
    else:
        data = {}
        data[u'js_conf'] = json.dumps({
            u'appId': OAUTH['facebook']['app_key'],
            u'canvasName': FACEBOOK_APP['canvas_name'],
            #~ u'userIdOnServer': None #self.user.user_id if self.user else None,
            u'userIdOnServer': initialization.user.user_id if initialization.user else None,
        })
        if request.method == 'POST':
            request.POST['user']
        data[u'canvas_name'] = FACEBOOK_APP['canvas_name']
        pass
        #~ return  render_to_response('hola.html',{'data':data}, context_instance=RequestContext(request))
        return  render_to_response('welcome.html',{'data':data}, context_instance=RequestContext(request))
    

@csrf_exempt
def dashboard(request):
    #~ setupVars(request)
    if request.method == 'POST':
        asd=BaseHandler
        
        data = {}
        data[u'js_conf'] = json.dumps({
            u'appId': OAUTH['facebook']['app_key'],
            u'canvasName': FACEBOOK_APP['canvas_name'],
            u'userIdOnServer': None #self.user.user_id if self.user else None,
        })
        
        data[u'canvas_name'] = FACEBOOK_APP['canvas_name']
        return  render_to_response('dashboard.html',{'data':data,'user':asd.facebook}, context_instance=RequestContext(request))
