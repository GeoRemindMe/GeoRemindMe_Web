# coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from userena.views import profile_detail as userena_profile_detail

@login_required
def dashboard(request):
    # TODO : (jneight) pintar timeline privado
    return HttpResponse('dashboard')

def profile_edit(request):
    pass

def profile_detail(request, username):
    # TODO : (jneight) pintar timeline publico
    return userena_profile_detail(request, username=username)
