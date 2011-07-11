# coding=utf-8
import base64
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template

from google.appengine.api import users

from georemindme.funcs import make_random_string
from models import User
from models_social import *
from models_acc import *
from forms import *
from exceptions import *
from funcs import init_user_session, get_next, login_func
from decorators import login_required
from geoauth.clients import facebook, twitter, google

"""
.. module:: views
    :platform: appengine
    :synopsis: Views for User model
"""

#===============================================================================
# REGISTER VIEW
#===============================================================================
def register(request):
    """**Descripción**: Recibe una petición de registro vía POST e intenta crear un usuario; en caso de éxito le enviará un email para confirmar su cuenta.
        
        :param request: array con un email y dos contraseñas
        :type request: array
		:return: En caso de éxito un :class:`geouser.models.User` y un formulario de registro. En caso de que no se reciba POST redirige al panel de registro
            
    """
    if request.method == 'POST':
        f = RegisterForm(request.POST, prefix='user_register')
        user = None
        if f.is_valid():
            user = f.save(language=request.session['LANGUAGE_CODE'])
            if user:
                messages.success(request, _("User registration complete, a confirmation email have been sent to %s. Redirecting to dashboard...") % user)
        return user, f
    return HttpResponseRedirect(reverse('georemindme.views.register_panel'))

#===============================================================================
# LOGIN VIEWS
#===============================================================================
def login(request):
    """**Descripción**: Recibe petición de autenticación vía POST y si los datos son correctos
        se llama a la función login_func que inicializa, crea la sesión y 
        devuelve un mensaje en caso de éxito.
        
        :return: En caso de recibir el POST devuelve un string con posibles errores y redirect con la URL a la que habría que dirigir. En caso contrario renderiza la plantilla de login.
            
    """
    
    if request.method == 'POST':
        f = LoginForm(request.POST, prefix='user_login')    
        error = ''
        redirect = ''
        if f.is_valid():
            error, redirect = login_func(request, f.cleaned_data['email'], f.cleaned_data['password'], f.cleaned_data['remember_me'])
        else:
            error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
        return error, redirect
    return render_to_response('webapp/login.html', {'login': True, 'next': request.path}, context_instance=RequestContext(request))

def login_google(request):
    """**Descripción**: Comprueba si ya te has dado de alta en la App con tu cuenta de Google
        para entrar automáticamente y sino pedirte permiso para hacerlo.
        Además en caso de éxito inicializa la sesión para dicho usuario.
        
       :return: En caso de exito llama a :py:func:`geouser.funcs.login_func` y redirige al panel. En caso contrario renderiza la plantilla de login.
    """
    ugoogle = users.get_current_user()
    if ugoogle:
        if request.user.is_authenticated():
            guser = GoogleUser.objects.get_by_id(ugoogle.user_id())
            if not guser:
                guser = GoogleUser.register(user=request.user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            if hasattr(request, 'facebook'):
                return HttpResponseRedirect(reverse('facebookApp.views.profile_settings'))    
            return HttpResponse(get_next(request))
        if not guser:#user is not registered, register it
            user = User.objects.get_by_email(ugoogle.email())
            if user:
                guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            else:
                user = User.register(email=ugoogle.email(), password=make_random_string(length=6))
                guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            init_user_session(request, user)
        else:#checks google account is confirmed, only load his account
            guser.update(ugoogle.email(), realname=ugoogle.nickname())
            init_user_session(request, guser.user)
        return HttpResponseRedirect(get_next(request))
    #not google user
    return HttpResponseRedirect(users.create_login_url(reverse('geouser.views.login_google')))
    
def login_facebook(request):
    """**Descripción**: Utiliza el `protocolo OAuth <http://oauth.net/>`_ para solicitar al 
        usuario que confirme que podemos usar sus sesión de Facebook para identificarlo.
        Así si el usuario está identificado en Facebook no necesitará
        rellenar el formulario de login de GeoRemindMe. :py:func:`.login_twitter`
        
        :return: En caso de exito redirige al panel y en caso contrario redirige al panel de login.
    """
    from geoauth.views import facebook_authenticate_request
    return facebook_authenticate_request(request)

def login_twitter(request):
    """**Descripción**: Utiliza el `protocolo OAuth <http://oauth.net/>`_ para solicitar al usuario que confirme
        que podemos usar sus sesión de Twitter para identificarlo.
        
        Así si el usuario está identificado en Twitter no necesitará
        rellenar el formulario de login de GeoRemindMe.
        
        :return: En caso de exito redirige al panel y en caso contrario redirige al panel de login.
    """
    from geoauth.views import authenticate_request
    return authenticate_request(request, 'twitter')

#===============================================================================
# LOGOUT VIEW
#===============================================================================
def logout(request):
    """**Descripción**: Elimina la sesión de usuario y redirige al usuario.
        
        :return: Redirige al usuario a donde le diga la función login_panel.
    """
    request.session.delete()
    return HttpResponseRedirect(reverse('georemindme.views.login_panel'))
    ##return HttpResponseRedirect(users.create_logout_url(reverse('georemindme.views.login_panel')))

#===============================================================================
# CONFIGURACION DE LA CUENTA, PRIVACIDAD, ETC.
#===============================================================================
@login_required
def update_profile(request):
    """**Descripción**: Actualiza el nombre de usuario y el avatar.
        
        :return: Solo devuelve errores si el proceso falla.
    """
    if request.method == 'POST':
        f = UserProfileForm(request.POST, prefix='user_settings_profile')
        if f.is_valid():
            updated = f.save(request.session['user'], file=request.POST['avatar'])
            if updated:
                return
        return f.errors
    
@login_required
def update_user(request):
    """**Descripción**: Permite actualizar el email y la contraseña.
        
        :return: Solo devuelve errores si el proceso falla.
    """
    if request.method == 'POST':
        f = UserForm(request.POST, prefix='user_settings')
        if f.is_valid():
            user = f.save()
            if user:
                return
        return f.errors
            

#===============================================================================
# DASHBOARD VIEW
#===============================================================================
@login_required
def dashboard(request):
    """**Descripción**: Permite actualizar el email y la contraseña.
        
        :return: Solo devuelve errores si el proceso falla.
    """
    if request.user.username is None or request.user.email is None:
        if request.method == 'POST':
            f = SocialUserForm(request.POST, prefix='user_set_username')
            if f.is_valid():
                user = f.save(request.session['user'])
                if user:
                    request.session['user'] = user
                    return HttpResponseRedirect(reverse('geouser.views.dashboard'))
        else:
            f = SocialUserForm(prefix='user_set_username', initial = { 
                                                                  'email': request.session['user'].email,
                                                                  'username': request.session['user'].username,
                                                                  })
        return render_to_response('webapp/socialsettings.html', {'form': f}, context_instance=RequestContext(request))
    return direct_to_template(request, 'webapp/dashboard.html')

def public_profile(request, username):
    """**Descripción**: Perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    profile_user = User.objects.get_by_username(username)
    if profile_user is None:
        raise Http404()
    settings = profile_user.settings
    profile = profile_user.profile
    counters = UserCounter.objects.get_by_id(profile_user.id, async=True)
    if request.user.is_authenticated():
        is_following = profile_user.is_following(request.user)
        is_follower = request.user.is_following(profile_user)
    else:
        is_following = None
        is_follower = None
    if is_following:  # el usuario logueado, sigue al del perfil
        timeline = UserTimeline.objects.get_by_id(profile_user.id, vis='shared')
    elif settings.show_timeline:
        timeline = UserTimeline.objects.get_by_id(profile_user.id)
    return render_to_response('webapp/publicprofile.html', {'profile': profile, 
                                                            'counters': counters.get_result(),
                                                            'timeline': timeline, 
                                                            'is_following': is_following,
                                                            'is_follower': is_follower, 
                                                            'show_followers': settings.show_followers,
                                                            'show_followings': settings.show_followings
                                                            }, context_instance=RequestContext(request))
    
    
#===============================================================================
# CONFIRM VIEW
#===============================================================================
def confirm(request, user, code):
    """**Descripción**: confirma el email de usuario
		
		:param user: nombre de usuario
		:type user: string
		:param code: código de confirmación
		:type code: string
		:return: En caso de que todo vaya correctamente solicitar identificarse al usuario. En caso contrario devuelve un mensaje de error
	"""
    user = base64.urlsafe_b64decode(user.encode('ascii'))
    u = User.objects.get_by_email_not_confirm(user)
    if u is not None:
        if u.confirm_user(code):
            msg = _("User %s confirmed. Please log in.") % user
            return render_to_response('webapp/confirmation.html', {'msg': msg}, context_instance=RequestContext(request))
    msg = _("Invalid user %s") % user
    return render_to_response('webapp/confirmation.html', {'msg': msg}, context_instance=RequestContext(request))

#===============================================================================
# REMIND PASSWORD VIEWS 
#===============================================================================
def remind_user(request):
    """**Descripción**: Resetea la contraseña de usuario
	"""
    if request.method == 'POST':
        f = EmailForm(request.POST, prefix='pass_remind')
        if f.is_valid():
            user = User.objects.get_by_email(f.cleaned_data['email'])
            if user is None:
                fail = _("Email doesn't exist")
                f._errors['email'] = f.error_class([fail])
            else:
                user.send_remind_code()
                msg = _("A confirmation mail has been sent to %s. Check mail") % user.email
                return render_to_response('webapp/user_pass.html', dict(msg=msg), context_instance=RequestContext(request))
    else:
        f = EmailForm(prefix='pass_remind')
    return render_to_response('webapp/user_pass.html', {'form': f}, context_instance=RequestContext(request))

def remind_user_code(request, user, code):
    """**Descripción**: Genera una nueva URL única para resetear la contraseña de usuario
    
    :param user: nombre de usuario
    :type user: string
    :param code: código único para recuperar contraseña
    :type code: int
	"""
    user = base64.urlsafe_b64decode(user.encode('ascii'))
    user = User.objects.get_by_email(user)
    if user is not None:
        try:
            user.reset_password(code)
            if request.method == 'POST':
                f = RecoverPassForm(request.POST, prefix='pass_recover')
                if f.is_valid():
                    user.reset_password(code, password=f.cleaned_data['password'])
                    msg = _("Password changed, please log in.")
                    return render_to_response('user_pass.html', {'msg': msg}, context_instance=RequestContext(request))
                else:
                    f = RecoverPassForm(prefix='pass_recover')
                msg = _("Set your new password.")
            return render_to_response('user_pass.html', {'form': f, 'msg': msg}, context_instance=RequestContext(request))
        except OutdatedCode, o:
            msg = _(o.message)
        except BadCode, i:
            msg = _(i.message)
    else:
        msg = _('Invalid user')
    return render_to_response('webapp/user_pass.html', {'msg': msg}, context_instance=RequestContext(request))


#===============================================================================
# FUNCIONES DE FOLLOWERS Y FOLLOWINGS
#===============================================================================
def get_followers(request, userid=None, username=None, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de followers de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado.
        
		:param userid: id del usuario (user.id)
		:type userid: string
		:param username: nombre del usuario (user.username)
		:type username: string
		:param page: número de página a mostrar
		:type page: int
		:param query_id: identificador de búsqueda
		:type query_id: int
		:return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    if userid is None and username is None:
        if request.session.get('user', None):
            return request.session['user'].get_followers(page=page, query_id=query_id)
        return None
    else:
        if userid:
            profile_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            profile_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(profile_key.name())
        if settings.show_followers:
            return User.objects.get_followers(userid=userid, username=username, page=page, query_id=query_id)
    return None
    
def get_followings(request, userid=None, username=None, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de followings de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado
        
		:param userid: id del usuario (user.id)
		:type userid: string
		:param username: nombre del usuario (user.username)
		:type username: string
		:param page: número de página a mostrar
		:type page: int
		:param query_id: identificador de búsqueda
		:type query_id: int
		:return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    if userid is None and username is None:
        if request.session.get('user', None):
            return request.session['user'].get_followings(page=page, query_id=query_id)
        return None
    else:
        if userid:
            user_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            user_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(user_key.name())
        if settings.show_followings:
            return User.objects.get_followings(userid=userid, username=username, page=page, query_id=query_id)
    return None
    
@login_required
def add_following(request, userid=None, username=None):
    """**Descripción**:	Añade un  nuevo usuario a la lista de following del usuario logeado
    
		:param userid: id del usuario (user.id)
		:type userid: string
		:param username: nombre del usuario (user.username)
		:type username: string
		:return: booleano con el resultado de la operación
    """
    return request.session['user'].add_following(followid=userid, followname=username)

@login_required
def del_following(request, userid=None, username=None):
    """**Descripción**: Borra un usuario de la lista de following del usuario logeado
		
		:param userid: id del usuario (user.id)
		:type userid: string
		:param username: nombre del usuario (user.username)
		:type username: string
		:return: boolean con el resultado de la operacion
    """
    return request.session['user'].del_following(followid=userid, followname=username)

@login_required
def get_contacts_google(request):
    """**Descripción**: Obtiene una lista con los contactos en gmail que
    el usuario puede seguir
    
    """
    if 'oauth_token' in request.GET:
        from geoauth.views import client_access_request
        client_access_request(request, 'google')
    from geoauth.clients.google import GoogleClient
    try:
        c = GoogleClient(user=request.user)
        contacts = c.get_contacts_to_follow()
    except:
        return HttpResponseRedirect(reverse('geouser.views.get_perms_google'))
    
    return render_to_response('webapp/contacts_google.html', {'contacts' : contacts, },
                              context_instance=RequestContext(request))

@login_required
def get_perms_google(request):
    """**Descripción**: Obtiene los permisos para acceder a los contactos de una cuenta de google
    
    """
    from geoauth.views import client_token_request
    return client_token_request(request, 'google', callback_url=request.build_absolute_uri(reverse('geouser.views.get_contacts_google') ))


@login_required
def get_friends_facebook(request):
    """**Descripción**: Obtiene una lista con los contactos en gmail que
    el usuario puede seguir
    
    """
    from geoauth.clients.facebook import *

    c = FacebookClient(user=request.user)
    return c.get_friends_to_follow()

@login_required
def get_perms_twitter(request):
    """**Descripción**: Obtiene los permisos para acceder a una cuenta de twitter
    
    """
    from geoauth.views import client_token_request
    return client_token_request(request, 'twitter', callback_url=request.build_absolute_uri(reverse('geouser.views.get_friends_twitter')))

@login_required
def get_friends_twitter(request):
    """**Descripción**: Obtiene una lista con los contactos en gmail que
    el usuario puede seguir
    
    """
    from geoauth.views import client_access_request
    if 'oauth_token' in request.GET:
        client_access_request(request, 'twitter')
    from geoauth.clients.twitter import *
    try:
        c = TwitterClient(user=request.user)
        contacts = c.get_friends_to_follow()
    except:
        return HttpResponseRedirect(reverse('geouser.views.get_perms_twitter'))
    
    return render_to_response('webapp/contacts_twitter.html', {'contacts' : contacts, },
                              context_instance=RequestContext(request))
    


#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
def get_timeline(request, userid = None, username = None, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de un usuario, si no se recibe userid o username, se obtiene la lista del usuario logueado
        
		:param userid: id del usuario (user.id)
		:type userid: string
		:param username: nombre del usuario (user.username)
		:type username: string
		:param page: número de página a mostrar
		:type page: int
		:param query_id: identificador de búsqueda
		:type query_id: int
		:return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad            
    """
    if userid is None and username is None:
        if request.session.get('user', None):
            return request.session['user'].get_timelineALL(page=page, query_id=query_id)
        return None
    else:
        if userid:
            user_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            user_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(user_key.name())
        if settings.show_timeline:
            return UserTimeline.objects.get_by_id(user_key.name(), page=page, query_id=query_id)
    return None

@login_required
def get_chronology(request, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de los followings del usuario logueado

		:param page: número de página a mostrar
		:type page: int
		:param query_id: identificador de búsqueda
		:type query_id: int
		:return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    return request.session['user'].get_chronology(page=page, query_id=query_id)

    
def get_avatar(request, username):
    user = User.objects.get_by_username(username)
    if user is None:
        raise Http404
    if user.profile.sync_avatar_with_facebook:
        if user.facebook_user is not None:
            return HttpResponseRedirect("https://graph.facebook.com/%s/picture/" % user.facebook_user.uid)
    else:
        email = user.email
        default = "http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
        size = 50
        # construct the url
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return HttpResponseRedirect(gravatar_url)