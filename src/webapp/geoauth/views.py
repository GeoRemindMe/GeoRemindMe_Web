# coding=utf-8

import libs.oauth2 as oauth2
from cgi import parse_qs

from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.urlresolvers import reverse

from geouser.forms import LoginForm
from geouser.decorators import login_required
from geouser.funcs import login_func, init_user_session
from server import OAUTH_Server
from exceptions import OAUTHException


#===============================================================================
# SERVIDOR, AUTORIZAR TOKENS A OTROS, ACCESO A RECURSOS, ETC.
#===============================================================================
@csrf_exempt
def token_request(request):
    """Generates a new token request"""
    try:
        server = OAUTH_Server()
        oauthToken = server.token_requested(request)
    except Exception, e:
        return HttpResponseBadRequest(e)
    return HttpResponse(oauthToken)


@csrf_exempt
def authorize_token_request(request):
    """A consumer wants to authorize a request token"""
    if not 'oauth_token' in request.GET:
        return HttpResponseBadRequest()
    else:
        if request.user.is_authenticated():
            server = OAUTH_Server()
            if request.method == 'POST':
                if 'accept' in request.POST:#el token ha sido aceptado
                    token = server.authorization_token_requested(request, request.user)
                    if token.callback is not None:#devolvemos al usuario al callback
                        return HttpResponseRedirect('%s?oauth_token=%s&oauth_verifier=%s' % (token.callback, token.key, token.verifier))
                    else:#no hay callback
                        # TODO: mirar si es una aplicacion por PIN
                        return HttpResponse('oauth_token=%s&oauth_verifier=%s' % (token.key, token.verifier))
                else:
                    return HttpResponseRedirect('/')
            else:
                appInfo = server.appInfo_requested(request.GET['oauth_token'])
                return render_to_response('oauth/authorization.html', {'appInfo' : appInfo}, context_instance=RequestContext(request))
        else:
            #el usuario necesita identificarse primero
            if request.method == 'POST':
                f = LoginForm(request.POST, prefix='user_login')
                
                if f.is_valid():
                    error, redirect = login_func(request, f.cleaned_data['email'], f.cleaned_data['password'], f.cleaned_data['remember_me'])
                    if error == '':#el usuario se ha identificado, recargamos la pagina
                        return HttpResponseRedirect(request.get_full_path())
                else:
                    error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
            else:
                error = ''
                f = LoginForm(prefix='user_login')
            return render_to_response('oauth/login.html', {'error': error, 'form':f}, context_instance=RequestContext(request))


@csrf_exempt
def access_token_request(request):
    """From a authorized request token, get a new access token"""
    try:
        server = OAUTH_Server()
        oauthToken = server.access_token_requested(request)
    except Exception, e:
        return HttpResponseBadRequest(e)
    return HttpResponse(oauthToken)


#=============================================================================== 
# CLIENTE, IDENTIFICACION CON OTROS SERVIDORES, ETC.
#=============================================================================== 
@login_required
def client_token_request(request, provider, callback_url=None):
    OAUTH = settings.OAUTH
    provider = provider.lower()
    consumer = oauth2.Consumer(OAUTH[provider]['app_key'], OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer)
    if callback_url is None:
        callback_url = OAUTH[provider]['callback_url']
    if provider.lower() == 'google':  # pasamos el scope con los permisos que queremos en google
        response, content = client.request('%s?scope=https://www.google.com/m8/feeds/' % OAUTH[provider]['request_token_url'], method="POST", callback=callback_url)
    else:
        response, content = client.request(OAUTH[provider]['request_token_url'], method="POST", callback=callback_url)
    if response['status'] != 200:
        raise Exception("Invalid response from server.")

    params = parse_qs(content, keep_blank_values=False)
    
    request.session[provider] = {'request_token' : {
                                                    'oauth_token_secret' : params['oauth_token_secret'][0], 
                                                    'oauth_token' : params['oauth_token'][0],
                                                    'oauth_callback_confirmed' : params['oauth_callback_confirmed'][0]
                                                    }
                                 }
    url = "%s?oauth_token=%s&oauth_callback=%s" % (OAUTH[provider]['authorization_url'],
        request.session[provider]['request_token']['oauth_token'], callback_url)
    
    return HttpResponseRedirect(url)


@csrf_exempt
def client_access_request(request, provider, next=None):
    provider = provider.lower()
    try:
        if not request.session[provider]['request_token']['oauth_token'] == request.GET.get('oauth_token') \
            and request.GET.get('oauth_verifier') :
            return HttpResponseRedirect(reverse('georemindme.views.home'))
    except:
        return HttpResponseRedirect(reverse('georemindme.views.home'))
    #lee el token recibido
    token = oauth2.Token(request.GET.get('oauth_token'), 
                         request.session[provider]['request_token']['oauth_token_secret'])
    token.set_verifier(request.GET.get('oauth_verifier'))
    
    consumer = oauth2.Consumer(settings.OAUTH[provider]['app_key'],
                               settings.OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer, token) 
    #lo intercambia por un token de acceso
    response, content = client.request(settings.OAUTH[provider]['access_token_url'], method="GET")
    if response['status'] != 200:
        raise Exception("Invalid response from server.")
    params = parse_qs(content, keep_blank_values=False)
    token = {   
                'oauth_token_secret' : params['oauth_token_secret'][0], 
                'oauth_token' : params['oauth_token'][0],
            }
    if provider == 'twitter':
        from clients.twitter import TwitterClient
        client = TwitterClient(token=oauth2.Token(token['oauth_token'], token['oauth_token_secret']))
        if request.user.is_authenticated():#usuario ya esta logeado, guardamos el token de su cuenta
            client.authorize(request.user, login = False if 'nologin' in request.GET else True)
        else:
            user = client.authenticate()
            init_user_session(request, user)
    
    elif provider == 'google':
        from clients.google import GoogleClient
        client = GoogleClient(token=oauth2.Token(token['oauth_token'], token['oauth_token_secret']))
        if request.user.is_authenticated():#usuario ya esta logeado, guardamos el token de su cuenta
            client.authorize(request.user)
        else:
            raise OAUTHException()
    else:
        raise OAUTHException("Invalid server.")
    if 'cls' in request.GET:
        return HttpResponseRedirect(reverse('geouser.views.close_window'))
    if next is None:
        next = reverse('geouser.views.dashboard')
    return HttpResponseRedirect(next)

    
#===============================================================================
# LOGIN WITH OAUTH
#===============================================================================
def authenticate_request(request, provider, callback_url=None, cls=False):
    #normalmente la diferencia con client_token_request es que peticion se hace a la url /authenticate en vez de /authorize
    OAUTH = settings.OAUTH
    provider = provider.lower()
    consumer = oauth2.Consumer(OAUTH[provider]['app_key'], OAUTH[provider]['app_secret'])
    client = oauth2.Client(consumer)
    if callback_url is None:
        callback_url = OAUTH[provider]['callback_url']
        if cls:
            callback_url = callback_url + '?cls'
    response, content = client.request(OAUTH[provider]['request_token_url'], method="POST", callback=callback_url)
    if response['status'] != 200:
        raise Exception("Invalid response from server.")
    params = parse_qs(content, keep_blank_values=False)
    request.session[provider] = {'request_token' : {
                                                    'oauth_token_secret' : params['oauth_token_secret'][0], 
                                                    'oauth_token' : params['oauth_token'][0],
                                                    'oauth_callback_confirmed' : params['oauth_callback_confirmed'][0]
                                                    }
                                 }
    url = "%s?oauth_token=%s&oauth_callback=%s" % (OAUTH[provider]['authenticate_url'],
        request.session[provider]['request_token']['oauth_token'], callback_url)

    return HttpResponseRedirect(url)


def facebook_authenticate_request(request,get="redirect", callback_url=None):
    OAUTH = settings.OAUTH
    if callback_url is None:
        callback_url = OAUTH['facebook']['callback_url']
    url = "%s?client_id=%s&redirect_uri=%s&scope=%s" % (
                                                        OAUTH['facebook']['authorization_url'], 
                                                        OAUTH['facebook']['app_key'], 
                                                        callback_url,
                                                        OAUTH['facebook']['scope']
                                                        )
    
    if get=="url":
        return url
    else:
        return HttpResponseRedirect(url)


def facebook_access_request(request, next=None):
    code = request.GET.get('code', None)
    if code is not None:
        OAUTH = settings.OAUTH
        url = "%s?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (
                                                                            OAUTH['facebook']['access_token_url'],
                                                                            OAUTH['facebook']['app_key'],
                                                                            OAUTH['facebook']['callback_url'],
                                                                            OAUTH['facebook']['app_secret'],
                                                                            code
                                                                            )
        response, content = oauth2.httplib2.Http().request(url)
        if response['status'] != 200:
            raise Exception("Invalid response from server.")
        params = parse_qs(content, keep_blank_values=False)
        token = {   
                'access_token' : params['access_token'][0], 
            }
        from clients.facebook import FacebookClient
        client = FacebookClient(access_token = token['access_token'])
        if request.user.is_authenticated():#usuario ya esta logeado, guardamos el token de su cuenta
            client.authorize(request.user)
        else:
            user = client.authenticate()
            init_user_session(request, user)
    if next is None:
        next = reverse('geouser.views.dashboard')
    return HttpResponseRedirect(next)
    
    
@login_required
def revocate_perms(request, provider):
    from models import OAUTH_Access
    token = OAUTH_Access.get_token_user(provider, request.user)
    if token is not None:
        socialUser = eval('request.user.%s_user' % token.provider)
        if socialUser is not None:
            socialUser.delete()
        token.delete()
    return HttpResponseRedirect(reverse('geouser.views.close_window'))
