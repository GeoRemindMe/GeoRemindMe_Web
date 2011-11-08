# coding=utf-8

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from userena import views as userena_views
from userena import settings as userena_settings

import views as profiles_views

urlpatterns = patterns('',
    # Ver dashboard
    url(r'^dashboard/$',
       profiles_views.dashboard,
       name='profiles_dashboard'),
    # Editar perfil
    url(r'^user/(?P<username>[\.\w]+)/edit/$',
       profiles_views.profile_edit,
       name='userena_profile_edit'),
    # Ver perfil
    url(r'^user/(?P<username>[\.\w]+)/$',
       profiles_views.profile_detail,
       name='userena_profile_detail'),
    url(r'^users/(?P<page>[0-9]+)/$',
       userena_views.profile_list,
       name='userena_profile_list_paginated'),
    url(r'^users/$',
       userena_views.profile_list,
       name='userena_profile_list'),
   )