# coding=utf-8

from datetime import timedelta, datetime
from google.appengine.api import users
from django.utils import simplejson
from django.conf import settings
from django.core.urlresolvers import reverse

from georemindme.models import  Point, User


def getAlertsJSON(alerts):
    
    return simplejson.dumps([{    'id': a.id,
                                'name': a.name,
                                'description':a.description,
                                'x':a.poi.point.lat,
                                'y':a.poi.point.lon,
                                'address':unicode(a.poi.address),
                                'starts':str(a.starts),
                                'ends':str(a.ends),
                                'donedate':str(a.done_when.strftime("%d%b")) if a.done_when else '',
                                'done':a.is_done(),
                                'distance':a.get_distance() }
                          for a in alerts if isinstance(a.poi,Point)])
    
def init_user_session(request, user, remember=True):
    """when a user logs in, we need to initialize a new session,
        save session in user, and save the user in the session
        
            :param request: The HTTP Request
            :type request: :class:`http.Request`
            :param user: User login
            :type user: :class:`georemindme.models.User`
            :param remember: True if the user wants to save his session
            :type remember: boolean
    """
    from appengine_utilities.sessions import Session
    lang = request.session['LANGUAGE_CODE']
    request.session = Session(set_cookie_expires=remember)#register the user with session
    request.session['LANGUAGE_CODE'] = lang#saved language
    user._session = request.session.get_ds_entity()
    from datetime import datetime
    user.last_login = datetime.now()
    if not user.profile: 
        from georemindme.models import UserProfile
        p = UserProfile(user=user)
        p.put()
    user.put()
    request.session['user'] = user
    
def login_func(request, f):
    """Login function
    
            :param request: The HTTP Request
            :type request: :class:`http.Request`
            :param f: Login form
            :type user: :class:`georemindme.forms.LoginForm`
    """
    from django.utils.translation import ugettext as _
    error = ''
    redirect = ''
    user = User.objects.get_by_email(f.cleaned_data['email'])
    if user:
        if user.is_google_account():
            redirect = users.create_login_url(reverse('georemindme.views.login_google'))
        elif user.check_password(f.cleaned_data['password']):

            if not user.is_confirmed() and user.created + timedelta(days=settings.NO_CONFIRM_ALLOW_DAYS) < datetime.now():
                user.send_confirm_code()
                error = _("Email not confirmed in %d days, your access isn't allowed.<br/>A new confirm email have been sent." % settings.NO_CONFIRM_ALLOW_DAYS)
            else:
                remember = f.cleaned_data['remember_me']
                init_user_session(request, user, remember=remember)
                redirect = reverse('georemindme.views.dashboard')
                
        else:
            error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
        if 'redirect_after_login' in request.POST:
            redirect = request.POST['redirect_after_login']
    else:
            request.session["attemp"] = request.session.get("attemp", 0) + 1
            error = _("The email/password you entered is incorrect<br/>Please make sure your caps lock is off and try again")
    return error, redirect
