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
from django.conf import settings

from decorators import login_required, admin_required, username_required
from geouser.models import User


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
            error = _("El email/contraseña que has introducido es incorrecto.<br/>Por favor asegúrate que no tienes las mayúsculas actividas e inténtalo de nuevo.")
        return error, redirect
<<<<<<< HEAD
    if '/m/' in request.path:
        return render_to_response('mobile/login.html', {'login': True, 'next': request.path}, context_instance=RequestContext(request))
    return render_to_response('webapp/login.html', {'login': True, 'next': request.path}, context_instance=RequestContext(request))
=======
    return render_to_response('mainApp/login.html', {'login': True, 'next': request.path}, context_instance=RequestContext(request))
>>>>>>> master


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
            else:
                guser.update(ugoogle.email(), realname=ugoogle.nickname())
        else:#user is not registered, register it
            from models import User
            user = User.objects.get_by_email(ugoogle.email())
            if user:
                guser = GoogleUser.objects.get_by_id(ugoogle.user_id())
                if guser is None:
                    guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
                else:
                    guser.update(ugoogle.email(), realname=ugoogle.nickname())
            else:
                from georemindme.funcs import make_random_string
                user = User.register(email=ugoogle.email(), password=make_random_string(length=6), confirmed=True)
                guser = GoogleUser.register(user=user, uid=ugoogle.user_id(), email=ugoogle.email(), realname=ugoogle.nickname())
            from funcs import init_user_session
            init_user_session(request, user)
        #checks google account is confirmed, only load his account
        from funcs import get_next
        return HttpResponseRedirect(get_next(request))
    return HttpResponseRedirect(users.create_login_url(reverse('geouser.views.login_google')))


def login_facebook(request):
    """**Descripción**: Utiliza el `protocolo OAuth <http://oauth.net/>`_ para solicitar al 
        usuario que confirme que podemos usar sus sesión de Facebook para identificarlo.
        Así si el usuario está identificado en Facebook no necesitará
        rellenar el formulario de login de GeoRemindMe. :py:func:`.login_twitter`
        
        :return: En caso de exito redirige al panel y en caso contrario redirige al panel de login.
    """
    from geoauth.views import facebook_authenticate_request
    if 'cls' in request.GET:
        return facebook_authenticate_request(request, callback_url=request.GET['callback_url'] if 'callback_url' in request.GET else None, cls=True)
    return facebook_authenticate_request(request, callback_url=request.GET['callback_url'] if 'callback_url' in request.GET else None)


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
    return authenticate_request(request, 'twitter', cls=cls)


#===============================================================================
# LOGOUT VIEW
#===============================================================================
def logout(request):
    """**Descripción**: Elimina la sesión de usuario y redirige al usuario.
        
        :return: Redirige al usuario a donde le diga la función login_panel.
    """
    request.session.delete()
    #from google.appengine.api import users
    return HttpResponseRedirect(reverse('georemindme.views.login_panel'))
    #return HttpResponseRedirect(users.create_logout_url(reverse('georemindme.views.login_panel')))


#===============================================================================
# CONFIGURACION DE LA CUENTA, PRIVACIDAD, ETC.
#===============================================================================
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
#@login_required
def dashboard(request, template='generic/dashboard.html'):
    """**Descripción**: Permite actualizar el email y la contraseña.
        
        :return: Solo devuelve errores si el proceso falla.
    """
    if not request.user.is_authenticated(): # ¡no uses el decorador!
        return login(request)
    if request.user.username is None:
        if request.user.email is None:
            from forms import SocialTwitterUserForm as formClass
        else:
            if request.user.google_user is None and request.user.facebook_user is None:
                from forms import SocialUserForm as formClass
            else:
                from forms import SocialFacebookGoogleUserForm as formClass
        if request.method == 'POST':
            f = formClass(request.POST, 
                               prefix='user_set_username', 
                               initial = { 'email': request.user.email,
                                           'username': request.user.username,
                                         }
                               )
            if f.is_valid():
                user = f.save(request.user)
                if user:
                    request.session['user'] = user
                    request.session.put()
                    response = HttpResponseRedirect(reverse('geouser.views.dashboard_contacts'))
                    # cookie de primer login
                    from time import time
                    from datetime import datetime
                    max_age = datetime.fromtimestamp(time() + settings.SESSION_COOKIE_AGE*2)
                    expires = max_age - datetime.now()
                    expires = expires.days * 86400 + expires.seconds
                    response.set_cookie('new_user_%s' % request.user.id, 
                                        '', 
                                        max_age=  60 * 60 * 24 * 7 * 52,
                                        domain=settings.SESSION_COOKIE_DOMAIN,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE
                                        )
                    return response
        else:
            f = formClass(prefix='user_set_username', 
                               initial = { 'email': request.user.email,
                                           'username': request.user.username,
                                         }
                               )
        return render_to_response('generic/create_social_profile.html',
                               {
                                'form': f
                                }, 
                               context_instance=RequestContext(request)
                              )
    #------------------------------------------------------------------------------ 
    import memcache
    friends = memcache.get('%sfriends_to_%s' % (memcache.version, request.user.key()))
    if friends is None: # lanzamos las peticiones asincronas
        handlers_rpcs, list_rpc=request.user.get_friends_to_follow(rpc=True)
    chronology = request.user.get_activity_timeline()
    # FIXME: CHAPUZA, LA PLANTILLA ESPERA RECIBIR EL QUERY_ID EN JSON :)
    from django.utils import simplejson
    chronology[0] = simplejson.dumps(chronology[0])
    if friends is None:
        # usuarios con mas sugerencias
        top_users = User.objects.get_top_users()
        friends = {}
        for user in top_users:
            if not user.key() == request.user.key() and not request.user.is_following(user):
                friends[user.id] = {'username': user.username,
                                    'id': user.id
                                    }
        # amigos de otras redes sociales
        friends = request.user._callback_get_friends_to_follow(handlers_rpcs, list_rpc, friends)
    return  render_to_response(template, {
                                          'friends_to_follow': friends,
                                          'chronology': chronology,
                                          } , RequestContext(request)
                               )
    
@login_required    
def dashboard_contacts(request):
    from geoalert.models import Suggestion
    top_users = User.objects.get_top_users()
    top_users_dict = []
    for user in top_users:
        if not user.key() == request.user.key() and not request.user.is_following(user):
            top_users_dict.append({'username': user.username,
                                'id': user.id,
                                'last_sugs': Suggestion.objects.get_by_last_created(limit=3,
                                                                                    user=user,
                                                                                    querier=request.user
                                                                                    ),
                                'counters': user.counters,
                                }
                                  )
    return render_to_response('generic/add_contacts.html',
                               {
                                'top_users': top_users_dict
                                }, 
                               context_instance=RequestContext(request)
                              )
    

@username_required
def public_profile(request, username, template='generic/profile.html'):
    """**Descripción**: Perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    from google.appengine.ext import db
    from georemindme.funcs import prefetch_refprops
    from geoalert.models import Suggestion
    from geoalert.views import get_suggestion
    if username.lower() == 'none':
        raise Http404()
    if request.user.is_authenticated() \
     and request.user.username is not None \
     and request.user.username.lower() == username.lower():
        # Si el usuario esta viendo su propio perfil
        profile = request.user.profile
        counters = request.user.counters_async()
        sociallinks = profile.sociallinks_async()
        timeline = request.user.get_profile_timeline()
#        from geoalert.api import get_suggestions_dict
#        suggestions_entity = get_suggestions_dict(request.user)
#        suggestions = [db.model_from_protobuf(s.ToPb()) for s in suggestions_entity]
#        suggestions = prefetch_refprops(suggestions, Suggestion.user, Suggestion.poi)
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
#        suggestions = get_suggestion(request, id=None,
#                                     wanted_user=profile_user,
#                                     page = 1, query_id = None
#                                     )
        
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
        if not request.user.is_authenticated():
            pos = template.rfind('.html')
            template = template[:pos] + '_anonymous' + template[pos:]
    return render_to_response(template, {'profile': profile, 
                                         'counters': counters.next(),
                                         'sociallinks': sociallinks.next(),
                                         'chronology': timeline, 
#                                         'suggestions': suggestions,
                                         'is_following': is_following,
                                         'is_follower': is_follower, 
                                         'show_followers': show_followers,
                                         'show_followings': show_followings
                                        }, context_instance=RequestContext(request))


@login_required
def edit_profile (request, template='generic/edit_profile.html'):
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
                request.session['user'] = modified
                if '/fb/' in template:
                    return HttpResponseRedirect('/fb/user/%s/' % request.user.username)
                else:
                    return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
        f = UserProfileForm(initial={'username': request.user.username,
                                     'email': request.user.email,
                                     'description': request.user.profile.description, 
                                     'sync_avatar_with': request.user.profile.sync_avatar_with, },
                            prefix='user_set_profile'
                            )
    return render_to_response(template, {'form': f}, context_instance=RequestContext(request))

@login_required
def profile_settings(request, template='generic/settings.html'):
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
@login_required    
def edit_settings(request, template="generic/edit_settings.html"):
    from geouser.forms import UserSettingsForm
    if request.method == 'POST':
        f = UserSettingsForm(request.POST, prefix='user_set_settings')
        if f.is_valid():
            f.save(request.user)
            request.session['LANGUAGE_CODE'] = request.user.settings.language
            if 'facebookApp' in template:
                return HttpResponseRedirect(reverse('facebookApp.views.profile_settings'))
            else:
                return HttpResponseRedirect(reverse('geouser.views.profile_settings'))
    else:
        f = UserSettingsForm(prefix='user_set_settings', initial = { 
                                                                  'time_notification_suggestion_follower': request.user.settings.time_notification_suggestion_follower,
                                                                  'time_notification_suggestion_comment': request.user.settings.time_notification_suggestion_comment,
                                                                  'time_notification_account': request.user.settings.time_notification_account,
                                                                  'show_public_profile': request.user.settings.show_public_profile,
                                                                  'language': request.user.settings.language,
                                                                  }
                             )
    return  render_to_response(template, {'profile': request.user.profile,
                                                    'settings': request.user.settings,
                                                    'settings_form': f,
                                                    }, context_instance=RequestContext(request)
                               )

@username_required
def followers_panel(request, username, template='generic/followers.html'):
    if request.user.is_authenticated() and username == request.user.username:
        followers=request.user.get_followers()
    else:
        from geouser.api import get_followers
        followers = get_followers(request.user, username=username)
    
    if not request.user.is_authenticated():
            pos = template.rfind('.html')
            template = template[:pos] + '_anonymous' + template[pos:]
    if followers is None:
        return  render_to_response(template, {'followers': [],
                                           'username_page':username
                                           },
                                           context_instance=RequestContext(request)
                               )
    return  render_to_response(template, {'followers': followers[1],
                                          'username_page':username,
                                          },
                                          context_instance=RequestContext(request)
                               )


@username_required
def followings_panel(request, username, template='generic/followings.html'):
    if request.user.is_authenticated() and username == request.user.username:
        followings=request.user.get_followings()
    else:
        from geouser.api import get_followings
        followings = get_followings(request.user, username=username)
    if not request.user.is_authenticated():
            pos = template.rfind('.html')
            template = template[:pos] + '_anonymous' + template[pos:]
    if followings is None:
        return  render_to_response(template, {'followings': [],
                                           'username_page':username
                                           },
                                           context_instance=RequestContext(request)
                               )
    return  render_to_response(template, {'followings': followings[1],
                                           'username_page':username
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
    if hasattr(request, 'session'):
        request.session.delete()
    import base64
    email = base64.urlsafe_b64decode(user.encode('ascii'))
    from models import User
    u = User.objects.get_by_email_not_confirm(email)
    if u is not None:
        if u.confirm_user(code):
            msg = _(u"La cuenta de %s ya esta confirmada, por favor, conectate.") % u.email
            return render_to_response('mainApp/confirmation.html', {'msg': msg}, context_instance=RequestContext(request))
        else:
            msg = _(u"Codigo de confirmacion incorrecto")
            return render_to_response('mainApp/confirmation.html', {'msg': msg}, context_instance=RequestContext(request))
    u = User.objects.get_by_email(email, keys_only=True)
    if u is not None:
        msg = _(u"La cuenta de %s ya esta confirmada, por favor, conectate.") % email
    else:
        msg = _(u"Usuario erroneo %s.") % email
    return render_to_response('mainApp/confirmation.html', {'msg': msg}, context_instance=RequestContext(request))


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
                fail = _(u"El correo no existe")
                f._errors['email'] = f.error_class([fail])
            else:
                user.send_remind_code()
                msg = _(u"Se ha enviado un correo de confirmación a %s. Por favor revisa tu correo") % user.email
                return render_to_response('mainApp/user_pass.html', dict(msg=msg), context_instance=RequestContext(request))
    else:
        f = EmailForm(prefix='pass_remind')
    return render_to_response('mainApp/user_pass.html', {'form': f}, context_instance=RequestContext(request))


def remind_user_code(request, user, code):
    """**Descripción**: Genera una nueva URL única para resetear la contraseña de usuario
    
    :param user: nombre de usuario
    :type user: string
    :param code: código único para recuperar contraseña
    :type code: int
	"""
    import base64
    email = base64.urlsafe_b64decode(user.encode('ascii'))
    from models import User
    user = User.objects.get_by_email(email)
    if user is not None:
        from exceptions import OutdatedCode, BadCode
        from forms import RecoverPassForm
        try:
            user.reset_password(code) # comprueba codigo valido
            if request.method == 'POST':
                f = RecoverPassForm(request.POST, prefix='pass_recover')
                if f.is_valid():
                    user.reset_password(code, password=f.cleaned_data['password'])
                    msg = _(u"Contraseña cambiada, por favor identifíquese.")
                    return render_to_response('mainApp/user_pass.html', {'msg': msg}, context_instance=RequestContext(request))
            else:
                f = RecoverPassForm(prefix='pass_recover')
                msg = _(u"Establece tu nueva contraseña.")
            return render_to_response('mainApp/user_pass.html', {'form': f, 'msg': msg}, context_instance=RequestContext(request))
        except OutdatedCode, o:
            msg = _(o.message)
        except BadCode, i:
            msg = _(i.message)
        except ValueError, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            msg = _(u"Contraseña invalida")
    else:
        msg = _(u"Usuario inválido")
    return render_to_response('mainApp/user_pass.html', {'msg': msg}, context_instance=RequestContext(request))


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

    return render_to_response('generic/contacts_google.html', {'contacts' : contacts, },
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
    if hasattr(request, 'facebook'):
        fb_client = request.facebook['client']
    else:
        from geoauth.clients.facebook import FacebookClient
        try:
            fb_client = FacebookClient(user=request.user)
        except:
            return None
    return fb_client.get_friends_to_follow()


@login_required
def get_perms_twitter(request):
    """**Descripción**: Obtiene los permisos para acceder a una cuenta de twitter
    
    """
    from geoauth.views import client_token_request
    return client_token_request(request, 'twitter', callback_url=request.build_absolute_uri(reverse('geouser.views.get_friends_twitter')+'?cls&nologin'))


@login_required
def get_friends_twitter(request):
    """**Descripción**: Obtiene una lista con los contactos en twitter que
    el usuario puede seguir
    
    """
    from geoauth.clients.twitter import TwitterClient
    try:
        c = TwitterClient(user=request.user)
        contacts = c.get_friends_to_follow()
    except:
        return HttpResponseRedirect(reverse('geouser.views.login_twitter'))
    
    return render_to_response('generic/contacts_twitter.html', {'contacts' : contacts, },
                              context_instance=RequestContext(request))
    
#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
@login_required
def notifications(request, template='generic/notifications.html'):
    timeline = request.user.get_notifications_timeline()
    # reset contador de notificaciones
    request.user.counters.set_notifications(-10)
    return  render_to_response(template, {
                                          'chronology': timeline
                                          } , RequestContext(request))


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
    default = "https://georemindme.appspot.com/static/facebookApp/img/no_avatar.png"
    size = 50
    # construct the url
    import hashlib
    import urllib
    gravatar_url = "https://secure.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return HttpResponseRedirect(gravatar_url)


def close_window(request):
    return render_to_response('generic/close_window.html', {}, context_instance=RequestContext(request))

@admin_required
def update(request):
    from google.appengine.ext.deferred import defer
    defer(__update_users)  # mandar email de notificacion
#    from geovote.models import VoteCounter
#    from geoalert.models import Event
#    from google.appengine.ext import db
#    counters = VoteCounter.all()
#    for v in counters:
#        v.instance_key = db.get(v.instance).key()
#        v.put()
    return HttpResponse('Updating users...')


def __update_users():
    from django.conf import settings
    from models import User
#    from models_acc import UserSocialLinks
#    generico = User.objects.get_by_username('georemindme')
    users = User.all()
    for user in users:
#        profile = user.profile
#        settings = user.settings
#        counters = user.counters
#        from models_acc import SearchConfigGooglePlaces
#        from google.appengine.ext import db
#        sociallinks = profile.sociallinks
#        if sociallinks is None:
#            sociallinks = UserSocialLinks(parent=user.profile, key_name='sociallinks_%s' % user.id)
#        sc = SearchConfigGooglePlaces.all().ancestor(settings).get()
#        if sc is None:
#            sc = SearchConfigGooglePlaces(parent=user.settings, key_name='searchgoogle_%d' % user.id)
        #db.put([profile, settings, sc, counters, sociallinks])
        user.put()
#        user.add_following(followid=generico.id)
#        generico.add_following(followid=user.id)


