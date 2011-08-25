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
    #raise Exception(session._session)
    if request.user.is_authenticated():
        return func(*args, **kwargs)
    from views import login
    return login(args[0])


@decorator
def login_forced(func, *args, **kwargs):
    querier = args[0]
    if querier.is_authenticated():
        return func(*args, **kwargs)
    from django.http import HttpResponseForbidden
    return HttpResponseForbidden()

    
@decorator
def admin_required(func, *args, **kwargs):
    session = args[0].session  # request es el primer parametro que pasamos
    user = session.get('user')
    if user and user.is_authenticated() and user.is_admin():
        return func(*args, **kwargs)
    from views import login
    return login(args[0])
