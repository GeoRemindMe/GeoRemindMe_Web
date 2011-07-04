# coding=utf-8

#===============================================================================
# Si aparece un error de can't import ugettext o similar en el servidor de desarrollo,
# debes cargar la pagina principal y luego ir a /admin/ :)
#===============================================================================

#===============================================================================
# APPENGINE_ADMIN no se integra demasiado bien con django, habria que reescribir
# todo el views.py para hacer que no usara el webapp.RequestHandler.
# Aqui hay un pequeño ejemplo con como se deberian sustituir, por si interesa
# http://blog.pamelafox.org/2010/09/porting-from-app-engine-webapp.html
#
# POR TANTO, LOS ADMIN MODELS QUE DEBEN APARECER EN LA ADMINISTRACION, SE CREARAN AQUI 
#===============================================================================

from model_register import ModelAdmin, register

from geouser.models import User
from geouser.models_social import SocialUser
from geouser.models_acc import UserSettings
from georpcjson.models import  _Report_Bug

class UserAdminForm(ModelAdmin):
    model = User
    listFields = ('id', 'username', 'email', 'has', 'created')
    editFields = ('email', 'username', 'password', 'has')
    readonlyFields = ('confirm_code', 'remind_code', 'date_remind', 'last_point', 'created', 'last_login')
    
class SocialUserAdminForm(ModelAdmin):
    model = SocialUser
    listFields = ('user', 'uid', '_class', 'created')
    editFields = ('uid', 'email')
    readonlyFields = ('_class', 'created')
    
class UserSettingsAdminForm(ModelAdmin):
    model = UserSettings
    listFields = ('parent', 'created')
    editFields = ('time_notification_account', 'time_notification_suggestion_follower', 'show_followers', 'show_followings', 'show_timeline', 'language')
    readonlyFields = ('created',)
    
class _Report_BugAdminForm(ModelAdmin):
    model = _Report_Bug
    listFields = ('user', 'msg', 'datetime', 'created')
    readonlyFields = ('user', 'msg', 'datetime', 'created')

# Register to admin site
register(UserAdminForm, SocialUserAdminForm, UserSettingsAdminForm, _Report_BugAdminForm)
