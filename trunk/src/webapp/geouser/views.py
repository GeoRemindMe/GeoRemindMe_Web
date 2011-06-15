# coding=utf-8
import base64
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template

from google.appengine.api import users
from google.appengine.ext import db


from georemindme.funcs import make_random_string
from models import User
from models_social import *
from models_acc import *
from forms import *
from exceptions import *
from funcs import init_user_session, get_next, login_func
from decorators import login_required
from geoauth import facebook, twitter

#===============================================================================
# REGISTER VIEW
#===============================================================================
def register(request):
    if request.method == 'POST':
        f = RegisterForm(request.POST, prefix='user_register')
        user = None
        if f.is_valid():
            user = f.save(language=request.session['LANGUAGE_CODE'])
            if user:
                messages.success(request, _("User registration complete, a confirmation email have been sent to %s. Redirecting to dashboard...") % user)
        return user, f
    return HttpResponseRedirect(reverse('georemindme.views.home'))

#===============================================================================
# LOGIN VIEWS
#===============================================================================
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST, prefix='user_login')    
        error = ''
        redirect = ''
        if f.is_valid():
            error, redirect = login_func(request, f.cleaned_data['email'], f.cleaned_data['password'], f.cleaned_data['remember_me'])
        else:
            error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
        return error, redirect
    return render_to_response('webapp/home.html', {'login': True, 'next': request.path}, context_instance=RequestContext(request))

def login_google(request):
    ugoogle = users.get_current_user()
    if ugoogle:
        guser = GoogleUser.objects.get_by_id(ugoogle.user_id())
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
    from geoauth.views import facebook_authenticate_request
    return facebook_authenticate_request(request)

    fbcookie = facebook.get_user_from_cookie(request.COOKIES)
    if fbcookie:
        fbuser = FacebookUser.objects.get_by_id(fbcookie['uid'])
        graph = facebook.GraphAPI(cookie["access_token"])
        profile = graph.get_object("me")
        if not fbuser:
            user = User.objects.get_by_email(profile['email'])
            if user:
                fbuser = FacebookUser.register(user=user, uid=profile['uid'], 
                                               email=profile['email'], realname=profile["name"],
                                               profile_url=profile["link"],
                                               access_token=cookie["access_token"])
            else:
                user = User.register(email=profile['email'], password=make_random_string(length=6))
                fbuser = FacebookUser.register(user=user, uid=profile['uid'], 
                                               email=profile['email'], name=profile["name"],
                                               profile_url=profile["link"],
                                               access_token=cookie["access_token"])
            init_user_session(request, user)
        else:
            fbuser.update(uid=profile['uid'], 
                               email=profile['email'], name=profile["name"],
                               profile_url=profile["link"],
                               access_token=cookie["access_token"])
            init_user_session(request, fbuser.user)
            return HttpResponseRedirect(get_next(request))
    return HttpResponseRedirect(reverse('georemindme.views.home'))

def login_twitter(request):
    from geoauth.views import authenticate_request
    return authenticate_request(request, 'twitter')

#===============================================================================
# LOGOUT VIEW
#===============================================================================
def logout(request):
    request.session.delete()
   
    return HttpResponseRedirect(users.create_logout_url(reverse('georemindme.views.home')))

#===============================================================================
# CONFIGURACION DE LA CUENTA, PRIVACIDAD, ETC.
#===============================================================================
@login_required
def update_profile(request):
    '''para actualizar username y avatar'''
    if request.method == 'POST':
        f = UserProfileForm(request.POST, prefix='user_settings_profile')
        if f.is_valid():
            updated = f.save(request.session['user'], file=request.POST['avatar'])
            if updated:
                return
        return f.errors
    
@login_required
def update_user(request):
    '''
    solo para actualizar email y contraseña'''
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
    if request.session['user'].username is None or request.session['user'].email is None:
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
    '''
    Perfil publico que veran los demas usuarios
    '''
    profile_key = User.objects.get_by_username(username, keys_only=True)
    if profile_key is None:
        raise Http404()
    settings = UserSettings.objects.get_by_id(profile_key.name(), async=True)
    profile = UserProfile.objects.get_by_id(profile_key.name(), async=True)
    counters = UserCounter.objects.get_by_id(profile_key.name(), async=True)
    if 'user' in request.session and request.session['user'].is_authenticated():
        is_following = UserFollowingIndex.all().ancestor(request.session['user'].key()).filter('following =', profile_key).get()
        is_follower = UserFollowingIndex.all().ancestor(profile_key).filter('following =', request.session['user'].key()).get()
    else:
        is_following = None
        is_follower = None
    settings = settings.get_result()
    if is_following:  # el usuario logueado, sigue al del perfil
        timeline = timeline = UserTimeline.objects.get_by_id(profile_key.name(), vis='shared')
    elif settings.show_timeline:
        timeline = UserTimeline.objects.get_by_id(profile_key.name())
    return render_to_response('webapp/publicprofile.html', {'profile': profile.get_result(), 'counters': counters.get_result(),
                                                            'timeline': timeline, 'is_following': is_following,
                                                            'is_follower': is_follower, 'show_followers': settings.show_followers,
                                                            'show_followings': settings.show_followings}
                              , context_instance=RequestContext(request))
    
    
#===============================================================================
# CONFIRM VIEW
#===============================================================================
def confirm(request, user, code):
    """Confirms a user's email"""
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
    """reset the pass for a user"""
    if request.method == 'POST':
        f = EmailForm(request.POST, prefix='pass_remind')
        if f.is_valid():
            user = User.objects.get_by_email(f.cleaned_data['email'])
            if not user:
                fail = _("Email doesn't exist")
                f._errors['email'] = f.error_class([fail])
            if user.is_google_account():
                return HttpResponseRedirect(reverse('georemindme.views.login_google'))
            if user.is_geouser():
                user.profile.send_remind_code()
                msg = _("A confirmation mail has been sent to %s. Check mail") % user.email
                return render_to_response('user_pass.html', dict(msg=msg), context_instance=RequestContext(request))
    else:
        f = EmailForm(prefix='pass_remind')
    return render_to_response('user_pass.html', {'form': f}, context_instance=RequestContext(request))

def remind_user_code(request, user, code):
    """allow to reset password link"""
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
    return render_to_response('user_pass.html', {'msg': msg}, context_instance=RequestContext(request))


#===============================================================================
# FUNCIONES DE FOLLOWERS Y FOLLOWINGS
#===============================================================================
def get_followers(request, userid=None, username=None, page=1, query_id=None):
    '''
        Obtiene la lista de followers de un usuario, si no se recibe userid o username,
        se obtiene la lista del usuario logueado
        
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    '''
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
    '''
        Obtiene la lista de followings de un usuario, si no se recibe userid o username,
        se obtiene la lista del usuario logueado
        
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    '''
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
    '''
    Añade un  nuevo usuario a la lista de following del usuario logeado
    
        :param userid: id del usuario (user.id)
        :type userid: :class:`string`
        :param username: nombre del usuario (user.username)
        :type username: :class:`string`
        :returns: boolean con el resultado de la operacion
    '''
    return request.session['user'].add_following(userid=userid, username=username)

@login_required
def del_following(request, userid=None, username=None):
    '''
    Borra un usuario de la lista de following del usuario logeado
    
        :param userid: id del usuario (user.id)
        :type userid: :class:`string`
        :param username: nombre del usuario (user.username)
        :type username: :class:`string`
        :returns: boolean con el resultado de la operacion
    '''
    return request.session['user'].del_following(userid=userid, username=username)

#===============================================================================
# FUNCIONES PARA TIMELINEs
#===============================================================================
def get_timeline(request, userid = None, username = None, page=1, query_id=None):
    '''
        Obtiene la lista de timeline de un usuario, si no se recibe userid o username,
        se obtiene la lista del usuario logueado
        
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    '''
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
    '''
        Obtiene la lista de timeline de los followings del usuario logueado

            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma (id, username), None si el usuario tiene privacidad
    '''
    return request.session['user'].get_chronology(page=page, query_id=query_id)

        
    
    
        
