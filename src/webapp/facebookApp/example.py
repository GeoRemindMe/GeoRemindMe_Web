# coding=utf-8

from geoauth.clients.facebook import *
from geoauth.views import facebook_authenticate_request
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from geouser import models_social
from uuid import uuid4

from settings import OAUTH, FACEBOOK_APP


"""Provides access to the active Facebook User2 in self.current_user

The property is lazy-loaded on first access, using the cookie saved
by the Facebook JavaScript SDK to determine the User2 ID of the active
User2. See http://developers.facebook.com/docs/authentication/ for
more information.
"""

def set_cookie(self, name, value, expires=None):
        """Set a cookie"""
        if value is None:
            value = 'deleted'
            expires = datetime.timedelta(minutes=-50000)
        jar = Cookie.SimpleCookie()
        jar[name] = value
        jar[name]['path'] = u'/'
        if expires:
            if isinstance(expires, datetime.timedelta):
                expires = datetime.datetime.now() + expires
            if isinstance(expires, datetime.datetime):
                expires = expires.strftime('%a, %d %b %Y %H:%M:%S')
            jar[name]['expires'] = expires
        self.response.headers.add_header(*jar.output().split(u': ', 1))

class CsrfException(Exception):
    pass
    
def init_csrf(request):
    """Issue and handle CSRF token as necessary"""
    
    csrf_token = request.session.get(u'c')
    if not csrf_token:
        csrf_token = str(uuid4())[:8]
        request.session['c']= csrf_token
        request.session['csrf_token']= csrf_token
    if request.method == u'POST' and \
            csrf_token != request.POST.get(u'_csrf_token'):
        raise CsrfException(u'Missing or invalid CSRF token.')

def registration_panel(request):
    args={}
    args[u'js_conf'] = json.dumps({
            u'appId': settings.OAUTH['facebook']['app_key'],
            u'canvasName': settings.FACEBOOK_APP['canvas_name'],
            #~ u'userIdOnServer': self.user.user_id if self.user else None,
        })
    args["permissions"]=settings.OAUTH['facebook']['scope']
    
    return args

@csrf_exempt
def login_panel(request):
    
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
                    return HttpResponseRedirect('/fb/dashboard')
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
def dashboard(request):

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
        args[u'js_conf'] = registration_panel(request)
    
        return  render_to_response('dashboard.html',args)
    else:
        return HttpResponseRedirect('/fb/')

@csrf_exempt
def login_panel2(request):
    #~ csrf_token=init_csrf(request);
    
    args={}
    args[u'js_conf'] = json.dumps({
            u'appId': settings.OAUTH['facebook']['app_key'],
            u'canvasName': settings.FACEBOOK_APP['canvas_name'],
            #~ u'userIdOnServer': self.user.user_id if self.user else None,
        })
    args["facebook_app_id"]=settings.OAUTH['facebook']['app_key']
    
    cookie = get_user_from_cookie(request.COOKIES)
    if cookie:
        raise Exception(cookie)
    
    if "user" in request.session:
        #Comprobamos si está autenticado a través de georemindme.appspot.com
        print request.session.data
        if request.session['user'].is_authenticated():        
            access_token=OAUTH_Access.get_token_user("facebook",request.user)
            if access_token is None:
                #Si no tenemos autorizacion de Facebook la pedimos
                return  render_to_response('example.html',args)
    elif not "current_user" in request.session or request.session["current_user"]==None:
            #Menu de instalacion de la AppRegister the App
            #~ raise Exception(request.session.data)
            #~ raise Exception(request.COOKIES)
            cookie = get_user_from_cookie(request.COOKIES)
            user=FacebookUser.objects.get_by_id(cookie["uid"])
            if user==None:
                fb_client=FacebookClient(cookie["access_token"])
                user=fb_client.authenticate()
                args['user']=user
                
            if cookie:
                access_token=OAUTH_Access.get_token(cookie["access_token"])
                if not access_token:
                    fb_client=FacebookClient(cookie["access_token"])
                    user=fb_client.authenticate()
                    args['user']=user
                    
            raise Exception(user.profile_url)
            scope=settings.OAUTH['facebook']['scope']
            register_url=facebook_authenticate_request(request,"url")
            args['permissions']=scope
            args['reg_url']=register_url
            return render_to_response('register.html',args)
    else:
        #Ver si está autenticado contra Facebook    
        #~ if not "current_user" in request.session or request.session["current_user"]==None:
            #~ request.session["current_user"] = None
        cookie = get_user_from_cookie(request.COOKIES)
        
        if cookie:
            access_token=OAUTH_Access.get_token(cookie["access_token"])
            #~ user = access_token.user
            #~ cookie["uid"]
            if not access_token:
                fb_client=FacebookClient(cookie["access_token"])
                user=fb_client.authenticate()
                if not fb_client.authorize(user):
                    #Se autoriza al usuario y si no existe se crea.
                    return HttpResponse("Error al crear el usuario con access token "+cookie["access_token"]);
                
                access_token=OAUTH_Access.get_token(cookie["access_token"])
        
            fb_client=FacebookClient(access_token.token_key)
            user = fb_client.get_user_info()
                        
            args["current_user"]=user;
            
        return  render_to_response('example.html',args)


