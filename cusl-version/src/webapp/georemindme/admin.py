# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""

from django import forms
from django.utils.translation import ugettext as _
from django.forms.extras.widgets import SelectDateWidget

from google.appengine.ext.db import djangoforms

from geoadmin.modelsAdmin import AdminModel, AdminForm, register
from models import GeoUser, GoogleUser

class UserAdminForm(AdminForm):
    key = forms.CharField(required=True, widget=forms.HiddenInput())
    email = forms.EmailField(required=True)
    password = forms.CharField(label=_("New password"), required=False,max_length=8, widget=forms.PasswordInput(attrs={'size':'10'}))
    password2 = forms.CharField(label=_("Repeat new password"), required=False,max_length=8, widget=forms.PasswordInput(attrs={'size':'10'}))
    active = forms.BooleanField(label=_("Is active"), required=False, widget=forms.CheckboxInput())
    confirmed = forms.BooleanField(label=_("Is confirmed"), required=False, widget=forms.CheckboxInput())
    admin = forms.BooleanField(label=_("Is admin"), required=False, widget=forms.CheckboxInput())
    
    def __init__(self, *args, **kwargs):
        
        try:
            initial = kwargs['initial']
            kwargs['initial'] = {
                                    'key': str(initial.key()),
                                    'email': initial.email,
                                    'created': initial.created,
                                    'active': initial.is_active(),
                                    'confirmed': initial.is_confirmed(),
                                    'admin': initial.is_admin(),
                                 }
        except:
            pass
        
        super(self.__class__, self).__init__(*args,**kwargs)
        
        
    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        if not self.cleaned_data:
            raise Exception()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Passwords can't have white spaces")
                self._errors['password'] = self.error_class([msg])
        
            if password != password2:
                msg = _("Passwords must be the same.")
                self._errors['password'] = self.error_class([msg])
            
        return cleaned_data
    
    def save(self):
        cleaned_data = self.cleaned_data
        from models import User
        u = User.objects.get_by_key(cleaned_data['key'])
        u.email = cleaned_data['email']
        if cleaned_data['password'] != '':
            u.password = cleaned_data['password']
            
        bool = cleaned_data.get('active', False)
        if (u.is_active() and bool) or (not u.is_active() and not bool):
            pass
        else:
            u.toggle_active()
                
        bool = cleaned_data.get('confirmed', False)
        if (u.is_confirmed() and bool) or (not u.is_confirmed() and not bool):
            pass
        else:
            u.toggle_confirmed()
    
        bool = cleaned_data.get('admin', False)
        if u.is_admin() and bool or (not u.is_admin() and not bool):
            pass
        else:
            u.toggle_admin()
                
        u.put()

class GeoUserAdmin(AdminModel):
    model = GeoUser
    description = 'Add, delete, modify the users'
    header_list = ['email','created',]
    form = UserAdminForm
    
class GoogleUserAdmin(AdminModel):
    model = GoogleUser
    description = 'Add, delete, modify the users with google account'
    header_list = ['email','created',]
    form = UserAdminForm

register(GeoUserAdmin, GoogleUserAdmin)
