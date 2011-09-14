# coding=utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

"""
.. module:: decorators
    :platform: appengine
    :synopsis: facebook_required decorator
    It is used to check if a user has perms with facebook
"""

from libs.decorator import *

@decorator
def facebook_required(func, *args, **kwargs):
    request = args[0]  # request es el primer parametro que pasamos
    if hasattr(request, 'facebook') \
        and request.user.is_authenticated() \
        and request.user.username is not None:
            return func(*args, **kwargs)
    return HttpResponseRedirect(reverse('facebookApp.views.login_panel'))