# coding=utf-8

"""
.. module:: Funcs
    :platform: appengine
    :synopsis: Funciones utiles utilizadas por geouser
"""

from django.conf import settings
from django.utils.translation import ugettext as _


def get_next(request):
    """Returns a url to redirect to after the login"""
    if 'next' in request.session:
        next = request.session['next']
        del request.session['next']
        return next
    elif 'next' in request.GET:
        return request.GET.get('next')
    elif 'next' in request.POST:
        return request.POST.get('next')
    else:
        from django.core.urlresolvers import reverse
        return reverse('geouser.views.dashboard')


def init_user_session(request, user, remember=False, from_rpc=False, is_from_facebook=False):
    """When a user logs in, we need to initialize a new session, save session in user, and save the user in the session

            :param request: The HTTP Request
            :type request: :class:`http.Request`
            :param user: User login
            :type user: :class:`georemindme.models.User`
            :param remember: True if the user wants to save his session
            :type remember: boolean
    """
    request.session.init_session(remember, lang=user.settings.language, user=user, from_rpc=from_rpc, is_from_facebook=is_from_facebook)
    request.user = user
    from datetime import datetime
    user.last_login = datetime.now()
    user.put()

def login_func(request, email = None, password = None, remember_me = False, user = None, from_rpc=False):
    """Login function

            :param request: The HTTP Request
            :type request: :class:`http.Request`
            :param f: Login form
            :type user: :class:`georemindme.forms.LoginForm`
    """
    error = ''
    redirect = ''
    if user is not None:
        redirect = get_next(request)
        init_user_session(request, user, remember=remember_me)
        return error, redirect
    from models import User
    from django.core.validators import validate_email
    try:
        validate_email(email.decode('utf8'))
        user = User.objects.get_by_email(email)
    except:
        user = User.objects.get_by_username(email)
    if user:
        if user.check_password(password):
            from datetime import datetime, timedelta
            if not user.is_confirmed() and (user.created + timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS)) < datetime.now():
                user.send_confirm_code()
                if from_rpc:
                    error = 0
                else:
                    error = _("Tu cuenta de correo no ha sido confirmada en %d días," 
                              "por lo que no puedes acceder."
                              "<br/>Te hemos reenviado el correo para que puedas activarla."
                              % settings.NO_CONFIRM_ALLOW_DAYS)
            else:
                redirect = get_next(request)
                init_user_session(request, user, remember=remember_me, from_rpc=from_rpc)
            return error, redirect
    request.session["attemp"] = request.session.get("attemp", 0) + 1
    if from_rpc:
        error = 1
    else:
        error = _(u"El email o la contraseña que has introducido es incorrecta \n"
                  + u"<br/>Por favor asegúrate que no tienes activadas las mayúsculas e inténtalo de nuevo")
    return error, redirect


def add_timeline_to_follower(user_key, follower_key, limit=10):
    from models_acc import UserTimeline, UserTimelineFollowersIndex
    from google.appengine.ext import db
    timeline = UserTimeline.all(keys_only=True).filter('user =', user_key).filter('_vis =', 'public').order('-modified').fetch(limit)
    indexes_to_save = []
    for t in timeline:
        if UserTimelineFollowersIndex.all(keys_only=True).ancestor(t).filter('followers =', follower_key).get() is not None:
            continue # ya esta el usuario como seguidor del timeline
        index = UserTimelineFollowersIndex.all().ancestor(t).order('-created').get()
        if index is None:  # no existen indices o hemos alcanzado el maximo
            index = UserTimelineFollowersIndex(parent=t)
        index.followers.append(follower_key)
        indexes_to_save.append(index)
    db.put(indexes_to_save)
    return True
