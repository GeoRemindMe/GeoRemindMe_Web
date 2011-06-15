# coding=utf-8

from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from google.appengine.ext import db

from models import User


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
        return reverse('geouser.views.dashboard')


def init_user_session(request, user, remember=True, from_rpc=False):
    """when a user logs in, we need to initialize a new session,
        save session in user, and save the user in the session

            :param request: The HTTP Request
            :type request: :class:`http.Request`
            :param user: User login
            :type user: :class:`georemindme.models.User`
            :param remember: True if the user wants to save his session
            :type remember: boolean
    """
    request.session.init_session(remember, lang=user.settings.language, user=user, from_rpc=from_rpc)
    user.last_login = datetime.now()
    user.put()

def login_func(request, email = None, password = None, remember_me = True, user = None, from_rpc=False):
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
        messages.success(request, _("Welcome, %s") % request.session['user'])
        return error, redirect
    user = User.objects.get_by_email(email)
    if user:
        if user.check_password(password):
            if not user.is_confirmed() and user.created + timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS) < datetime.now():
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
                messages.success(request, _("Welcome, %s") % request.session['user'])
            return error, redirect
    request.session["attemp"] = request.session.get("attemp", 0) + 1
    if from_rpc:
        error = 1
    else:
        error = _("The email/password you entered is incorrect"
                  "<br/>Please make sure your caps lock is off and try again")
    return error, redirect


