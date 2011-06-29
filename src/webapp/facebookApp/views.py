# coding=utf-8

from geoauth.clients.facebook import *
from geoauth.views import facebook_authenticate_request
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from geouser import models_social
from uuid import uuid4
from django.utils.decorators import decorator_from_middleware
#Para redireccionar sin necesidad de hacer otra petición HTTP
from django.core.urlresolvers import reverse
#~ from django.utils.decorators import decorator_from_middleware
#~ from facebookApp.facebook.djangofb import FacebookMiddleware
#~ import facebookApp.facebook.djangofb as facebook
from geouser.funcs import init_user_session

from settings import OAUTH, FACEBOOK_APP

from geouser.forms import *
from django.template import RequestContext




"""Provides access to the active Facebook User2 in self.current_user

The property is lazy-loaded on first access, using the cookie saved
by the Facebook JavaScript SDK to determine the User2 ID of the active
User2. See http://developers.facebook.com/docs/authentication/ for
more information.
"""



def registration_panel(request):
    args={}
    args['js_conf'] = json.dumps({
            u'appId': settings.OAUTH['facebook']['app_key'],
            u'canvasName': settings.FACEBOOK_APP['canvas_name'],
            #~ u'userIdOnServer': self.user.user_id if self.user else None,
        })
    args["permissions"]=settings.OAUTH['facebook']['scope']
    
    return args

@csrf_exempt
#~ @decorator_from_middleware(FacebookMiddleware)
#~ @facebook.require_login()
def login_panel(request):
    
    if request.session['user'].username is None or request.session['user'].email is None:
        #~ raise Exception(request.POST.get('id_user_set_username-username'))
        if request.method == 'POST':
            #~ raise Exception("Username=%s, email=%s"%(request['id_user_set_username-username'],request.session['user'].email))
            f = SocialUserForm(request.POST, prefix='user_set_username')
            if f.is_valid():
                user = f.save(request.session['user'])
                if user:
                    request.session['user'] = user
                    return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
        else:
            
            f = SocialUserForm(prefix='user_set_username', initial = { 
                                                                  'email': request.session['user'].email,
                                                                  'username': request.session['user'].username,
                                                                  })
        return render_to_response('webapp/socialsettings.html', {'form': f}, context_instance=RequestContext(request))
    
    #~ raise Exception("Username=%s, email=%s"%(request.session['user'].username,request.session['user'].email))
    
    
    if u'signed_request' in request.POST:        
        data = parse_signed_request(request.POST['signed_request'])
        #~ raise Exception (data)
        cookie = get_user_from_cookie(request.COOKIES)
        #~ raise Exception(cookie)
        if 'user_id' in data:
            # Actualizamos los datos de usuario
            if cookie is not None and data['user_id'] == cookie["uid"]:
                fb_client=FacebookClient(cookie["access_token"])
                if not fb_client.token_is_valid():
                    #~ raise Exception("Aasdasd %s"%cookie)
                    user=FacebookUser.objects.get_by_id(cookie["uid"])
                    OAUTH_Access.remove_token(user, 'facebook')
                    args=registration_panel(request)
                    return render_to_response('register.html',args)

                else:
                    #~ raise Exception("Aasdasd2 %s"%cookie)
                    #~ raise Exception("Username=%s"%request.user.username)
                    user=FacebookUser.objects.get_by_id(cookie["uid"])
                    if not request.user.is_authenticated():
                        init_user_session(request,user.user)
                    return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
            else:
                #~ raise Exception("Aquí entro? ",cookie["uid"])
                pass
        else:
            #No hay user_ide la cookie
            pass
            #~ raise Exception("Aquí entro?2")
    
    #Identificarse o registrarse
    args=registration_panel(request)
    return render_to_response('register.html',args)
    


@csrf_exempt
#~ @decorator_from_middleware(FacebookMiddleware)
#~ @facebook.require_login()
def dashboard(request):
    cookie = get_user_from_cookie(request.COOKIES)
    
    if cookie:
        
        #Comprobamos que el toque es aún válido
        fb_client=FacebookClient(cookie["access_token"])
        #~ raise Exception(fb_client.consumer.access_token)
        if not fb_client.token_is_valid():
            #Si el usuario ya no tiene instalada la app lo lleva a instalar
            args=registration_panel(request)
            return HttpResponseRedirect('/fb/')
        
        
        access_token=OAUTH_Access.get_token(cookie["access_token"])
        if not access_token:
            # Autentica al usuario con cookie["access_token"] y si no 
            # existe tal usuario lo crea y lo devuelve           
            fb_client=FacebookClient(cookie["access_token"])
            user=fb_client.authenticate()
            access_token=OAUTH_Access.get_token(cookie["access_token"])
    
        else:
            fb_client=FacebookClient(access_token.token_key)
            fb_client.authorize()
        
        user = fb_client.get_user_info()            
        
        args={}
        args["current_user"]=user;
        #~ raise Exception(user)
        args['js_conf'] = registration_panel(request)
        
        #~ friends=fb_client.get_friends()
        #~ args['friends']=friends['data']
        #~ raise Exception(friends)
        
        friends_to_follow=fb_client.get_friends_to_follow()
        args['friends_to_follow']=friends_to_follow
        
        followers=request.user.get_followers()
        args['followers']=followers[1]
        
        followings=request.user.get_followings()
        args['followings']=followings[1]
        #~ raise Exception(friends_to_follow)
        
        return  render_to_response('dashboard.html',args)
    else:
        return HttpResponseRedirect('/fb/')

@csrf_exempt
def user_profile(request, username):
    
    user=User.objects.get_by_username(username)
    #~ raise Exception(user.__dict__)
    return  render_to_response('public_profile.html',{'user':user})

@csrf_exempt
#~ @decorator_from_middleware(FacebookMiddleware)
#~ @facebook.require_login()
def profile_settings(request):
    cookie = get_user_from_cookie(request.COOKIES)
    if cookie:
        
        #Comprobamos que el toque es aún válido
        fb_client=FacebookClient(cookie["access_token"])
        if not fb_client.token_is_valid():
            #Si el usuario ya no tiene instalada la app lo lleva a instalar
            args=registration_panel(request)
            return HttpResponseRedirect('/fb/')
        
        
        access_token=OAUTH_Access.get_token(cookie["access_token"])
        if not access_token:
            # Autentica al usuario con cookie["access_token"] y si no 
            # existe tal usuario lo crea y lo devuelve           
            fb_client=FacebookClient(cookie["access_token"])
            user=fb_client.authenticate()
            access_token=OAUTH_Access.get_token(cookie["access_token"])
    
        else:
            fb_client=FacebookClient(access_token.token_key)
            fb_client.authorize()
        
        user = fb_client.get_user_info()            
        
        args={}
        args["current_user"]=user;
        #~ raise Exception(user)
        args['js_conf'] = registration_panel(request)
    
        return  render_to_response('profile.html',args)
    else:
        return HttpResponseRedirect('/fb/')
    