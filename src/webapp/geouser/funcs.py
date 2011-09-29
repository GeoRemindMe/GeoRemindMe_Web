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
            if not user.is_confirmed() and (user.created + timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS)) > datetime.now():
                user.send_confirm_code()
                if from_rpc:
                    error = 0
                else:
                    error = _("Email no confirmed in %d days," 
                              "your access isn't allowed."
                              "<br/>A new confirm email have been sent."
                              % settings.NO_CONFIRM_ALLOW_DAYS)
            else:
                redirect = get_next(request)
                init_user_session(request, user, remember=remember_me, from_rpc=from_rpc)
            return error, redirect
    request.session["attemp"] = request.session.get("attemp", 0) + 1
    if from_rpc:
        error = 1
    else:
        error = _("The email/password you entered is incorrect"
                  "<br/>Please make sure your caps lock is off and try again")
    return error, redirect
