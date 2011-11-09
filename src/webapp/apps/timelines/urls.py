# coding=utf-8

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

import views as timelines_views


urlpatterns = patterns('',
    # Editar perfil
    url(r'^settings/edit/$',
       timelines_views.settings_edit,
       name='timelines_settings_edit'),
    # Ver perfil
    url(r'^settings/$',
       timelines_views.settings_detail,
       name='timelines_settings_detail'),
   )