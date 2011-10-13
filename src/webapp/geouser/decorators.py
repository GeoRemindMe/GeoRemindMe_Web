# coding=utf-8

"""
.. module:: decorators
    :platform: appengine
    :synopsis: login_required decorator
    It is used to check if a user is logged in or not
"""

from libs.decorator import decorator

@decorator
def login_required(func, *args, **kwargs):
    request = args[0]  # request es el primer parametro que pasamos
    if request.user.is_authenticated():
        if request.user.username is not None:
            return func(*args, **kwargs)
        else: # falta el nombre de usuario, redirigimos al panel
            from views import dashboard
            return dashboard(request, *args, **kwargs)
    from views import login
    return login(args[0])


@decorator
def login_forced(func, *args, **kwargs):
    querier = args[0]
    if querier.is_authenticated() and querier.username is not None:
        return func(*args, **kwargs)
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden()

    
@decorator
def admin_required(func, *args, **kwargs):
    from google.appengine.api import users
    if users.is_current_user_admin():
        return func(*args, **kwargs)
    from views import login
    return login(args[0])


@decorator
def username_required(func, *args, **kwargs):
    request = args[0]  # request es el primer parametro que pasamos
    if request.user.is_authenticated() and request.user.username is None:
        from views import dashboard
        return dashboard(*args, **kwargs)
    return func(*args, **kwargs)
    


