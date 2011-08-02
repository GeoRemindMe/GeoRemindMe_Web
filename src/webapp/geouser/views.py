# coding=utf-8

"""
.. module:: views
    :platform: appengine
    :synopsis: Views for User model
"""


from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from decorators import login_required


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
        from forms import RegisterForm
        f = RegisterForm(request.POST, prefix='user_register')
        user = None
        if f.is_valid():
            user = f.save(language=request.session['LANGUAGE_CODE'])
            if user:
                from django.contrib import messages
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
        from forms import LoginForm
        f = LoginForm(request.POST, prefix='user_login')    
        error = ''
        redirect = ''
        if f.is_valid():
            from funcs import login_func
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
    from google.appengine.api import users
    from models_social import GoogleUser
    ugoogle = users.get_current_user()
    if ugoogle:
        if request.user.is_authenticated():
            guser = GoogleUser.objects.get_by_id(ugoogle.user_id())
            if not guser:
                guser = GoogleUser.register(user=request.user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            if hasattr(request, 'facebook'):
                return HttpResponseRedirect(reverse('facebookApp.views.profile_settings'))
            from funcs import get_next
            return HttpResponse(get_next(request))
        if not guser:#user is not registered, register it
            from models import User
            user = User.objects.get_by_email(ugoogle.email())
            if user:
                guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            else:
                from georemindme.funcs import make_random_string
                user = User.register(email=ugoogle.email(), password=make_random_string(length=6))
                guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            from funcs import init_user_session
            init_user_session(request, user)
        else:#checks google account is confirmed, only load his account
            guser.update(ugoogle.email(), realname=ugoogle.nickname())
            from funcs import init_user_session
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
    if 'cls' in request.GET:
        cls = True
        #callback_url = request.build_absolute_uri(reverse('geouser.views.close_window'))
    else:
        cls = False
        #callback_url=None
    from geoauth.views import authenticate_request
    #client_token_request(request, 'twitter', callback_url=callback_url)
    return authenticate_request(request, 'twitter', cls=True)


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
        from forms import UserProfileForm
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
        from forms import UserForm
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
def dashboard(request, template='webapp/dashboard.html'):
    """**Descripción**: Permite actualizar el email y la contraseña.
        
        :return: Solo devuelve errores si el proceso falla.
    """
    friends_to_follow=request.user.get_friends_to_follow()
    followers=request.user.get_followers()
    followings=request.user.get_followings()
    chronology = request.user.get_activity_timeline()
    return  render_to_response(template, {'friends_to_follow': friends_to_follow,
                                                  'followers': followers,
                                                  'followings': followings, 
                                                  'chronology': chronology,
                                                  } , RequestContext(request)
                               )


def public_profile(request, username, template='webapp/profile.html'):
    """**Descripción**: Perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    from geoalert.views import get_suggestion
    if request.user.username.lower() == username.lower():
        # Si el usuario esta viendo su propio perfil
        profile = request.user.profile
        counters = request.user.counters_async()
        sociallinks = profile.sociallinks_async()
        timeline = request.user.get_profile_timeline()
        suggestions = get_suggestion(request, id=None,
                                     wanted_user=request.user,
                                     page = 1, query_id = None
                                     )
        is_following = True
        is_follower = True
        show_followers = True
        show_followings = True
    else:
        # Si esta viendo el perfil de otro
        from geouser.models import User
        profile_user = User.objects.get_by_username(username)
        if profile_user is None:
            raise Http404()
        counters = profile_user.counters_async()#UserCounter.objects.get_by_id(profile_user.id, async=True)
        
        settings = profile_user.settings
        profile = profile_user.profile
        sociallinks = profile.sociallinks_async()
        suggestions = get_suggestion(request, id=None,
                                     wanted_user=profile_user,
                                     page = 1, query_id = None
                                     )
        
        if request.user.is_authenticated():
            is_following = profile_user.is_following(request.user)
            is_follower = request.user.is_following(profile_user)
        else:
            is_following = None
            is_follower = None
        if is_following or settings.show_timeline:  # el usuario logueado, sigue al del perfil
            timeline = profile_user.get_profile_timeline(querier=request.user)
        show_followers = settings.show_followers,
        show_followings = settings.show_followings
    
    return render_to_response(template, {'profile': profile, 
                                                'counters': counters.next(),
                                                'sociallinks': sociallinks.next(),
                                                'chronology': timeline, 
                                                'suggestions': suggestions,
                                                'is_following': is_following,
                                                'is_follower': is_follower, 
                                                'show_followers': show_followers,
                                                'show_followings': show_followings
                                                }, context_instance=RequestContext(request))


@login_required
def edit_profile (request, template='webapp/edit_profile.html'):
    """**Descripción**: Edición del perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    from geouser.forms import UserProfileForm
    if request.method == 'POST':
        f = UserProfileForm(request.POST, prefix='user_set_profile')
        if f.is_valid():
            modified = f.save(user=request.user)
            if modified:
                return HttpResponseRedirect('/fb/user/%s/' % request.user.username)

    else:
        f = UserProfileForm(initial={'username': request.user.username,
                                     'email': request.user.email,
                                     'description': request.user.profile.description, 
                                     'sync_avatar_with': request.user.profile.sync_avatar_with, },
                            prefix='user_set_profile'
                            )
    return render_to_response(template, {'form': f}, context_instance=RequestContext(request))

@login_required
def profile_settings(request, template='webapp/settings.html'):
    counters = request.user.counters_async()
    has_twitter = True if request.user.twitter_user is not None else False
    has_google = True if request.user.google_user is not None else False
    
    return  render_to_response(template,{'counters': counters.next(),
                                               'profile': request.user.profile,
                                               'has_twitter': has_twitter,
                                               'has_google': has_google,
                                               'settings': request.user.settings,
                                                },
                                            context_instance=RequestContext(request)
                                )
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
    import base64
    user = base64.urlsafe_b64decode(user.encode('ascii'))
    from models import User
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
    """
        **Descripción**: Resetea la contraseña de usuario
	"""
    from forms import EmailForm
    if request.method == 'POST':
        f = EmailForm(request.POST, prefix='pass_remind')
        if f.is_valid():
            from models import User
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
    import base64
    user = base64.urlsafe_b64decode(user.encode('ascii'))
    from models import User
    user = User.objects.get_by_email(user)
    if user is not None:
        from exceptions import OutdatedCode, BadCode
        try:
            user.reset_password(code)
            if request.method == 'POST':
                from forms import RecoverPassForm
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
        from models import User
        from models_acc import UserSettings
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
        from models import User
        from models_acc import UserSettings
        if userid:
            user_key = User.objects.get_by_id(userid, keys_only=True)
        elif username:
            user_key = User.objects.get_by_username(username, keys_only=True)
        settings = UserSettings.objects.get_by_id(user_key.name())
        if settings.show_followings:
            return User.objects.get_followings(userid=userid, username=username, page=page, query_id=query_id)
    return None


@login_required
def get_friends(request):
    users = request.user.get_friends().get_result()
    if len(users) > 0:
        return [(u.id, u.username) for u in users]
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
        if 'cls' in request.GET:
            return HttpResponseRedirect(reverse('geouser.views.close_window'))
    
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
    return client_token_request(request, 'google', callback_url=request.build_absolute_uri(reverse('geouser.views.get_contacts_google')+'?cls' ))


@login_required
def get_friends_facebook(request):
    """**Descripción**: Obtiene una lista con los contactos en gmail que
    el usuario puede seguir
    
    """
    from geoauth.clients.facebook import FacebookClient
    c = FacebookClient(user=request.user)
    return c.get_friends_to_follow()


@login_required
def get_perms_twitter(request):
    """**Descripción**: Obtiene los permisos para acceder a una cuenta de twitter
    
    """
    from geoauth.views import client_token_request
    return client_token_request(request, 'twitter', callback_url=request.build_absolute_uri(reverse('geouser.views.get_friends_twitter')+'?cls&nologin'))


@login_required
def get_friends_twitter(request):
    """**Descripción**: Obtiene una lista con los contactos en gmail que
    el usuario puede seguir
    
    """
    from geoauth.views import client_access_request
    if 'oauth_token' in request.GET:
        client_access_request(request, 'twitter')
        if 'cls' in request.GET:
            return HttpResponseRedirect(reverse('geouser.views.close_window'))
    from geoauth.clients.twitter import TwitterClient
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
def get_profile_timeline(request, userid = None, username = None, page=1, query_id=None):
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
        if request.user.is_authenticated():
            return request.user.get_profile_timeline(page=page, query_id=query_id)
        return None
    else:
        from models import User
        if userid:
            user_profile = User.objects.get_by_id(userid)
        elif username:
            user_profile = User.objects.get_by_username(username)
        if user_profile.settings.show_timeline:
            return user_profile.get_profile_timeline(page=page, query_id=query_id, querier=request.user)
    return None


@login_required
def notifications(request, template='webapp/notifications.html'):
    timeline = request.user.get_notifications_timeline()
    # reset contador de notificaciones
    request.user.counters.set_notifications(-request.user.counters.notifications)
    return  render_to_response(template, {
                                          'chronology': timeline
                                          } , RequestContext(request))


@login_required
def get_activity_timeline(request, page=1, query_id=None):
    """**Descripción**: Obtiene la lista de timeline de actividad del usuario logueado

        :param page: número de página a mostrar
        :type page: int
        :param query_id: identificador de búsqueda
        :type query_id: int
        :return: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    """
    return request.user.get_activity_timeline(page=page, query_id=query_id)

    
def get_avatar(request, username):
    from models import User
    user = User.objects.get_by_username(username)
    if user is None:
        raise Http404
    if user.profile.sync_avatar_with == 'facebook':
        if user.facebook_user is not None:
            return HttpResponseRedirect("https://graph.facebook.com/%s/picture/" % user.facebook_user.uid)
    elif user.profile.sync_avatar_with == 'twitter':
        if user.twitter_user is not None:
            return HttpResponseRedirect(user.twitter_user.picurl)

    email = user.email
    default = "http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
    size = 50
    # construct the url
    import hashlib
    import urllib
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return HttpResponseRedirect(gravatar_url)


def close_window(request):
    return render_to_response('webapp/close_window.html', {}, context_instance=RequestContext(request))


def update(request):
    from models import User
    users = User.all()
    for user in users:
        profile = user.profile
        settings = user.settings
        counters = user.counters
        from models_acc import SearchConfigGooglePlaces
        from google.appengine.ext import db
        sc = SearchConfigGooglePlaces.all().ancestor(settings).get()
        if sc is None:
            sc = SearchConfigGooglePlaces(parent=user.settings, key_name='searchgoogle_%d' % user.id)
        db.put([profile, settings, sc, counters])
        
    return HttpResponse()
