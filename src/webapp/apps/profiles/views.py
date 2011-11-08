# coding=utf-8

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from userena.views import profile_detail as userena_profile_detail
from userena.views import profile_edit as userena_profile_edit
from forms import UserProfileForm

@login_required
def dashboard(request):
    # TODO : (jneight) pintar timeline privado
    return HttpResponse('dashboard')

@login_required
def profile_edit(request, username):
    form = UserProfileForm
    return userena_profile_edit(request, 
                                username=username, 
                                edit_profile_form=form)

def profile_detail(request, username):
    # TODO : (jneight) pintar timeline publico
    return userena_profile_detail(request, username=username)
