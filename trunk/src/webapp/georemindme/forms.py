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

from google.appengine.ext.db import GeoPt, NotSavedError

from models import Alert,Point, GeoUser
from widgets import LocationWidget

MAX_LENGTH = 10
MIN_LENGTH = 6
PWD_LENGTH = 12

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)
    
class RecoverPassForm(forms.Form):
    password = forms.CharField(required=True,max_length=MAX_LENGTH, min_length=MIN_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    password2 = forms.CharField(label=_("Repeat password"), required=True, min_length=MIN_LENGTH, max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    
    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
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

class LoginForm(forms.Form):
    """
        Form for the login process
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    remember_me = forms.BooleanField(label=_("Remember me?"), required=False, widget=forms.CheckboxInput())
    

class RegisterForm(forms.Form):
    """
        Form for the register process
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,max_length=MAX_LENGTH, min_length=MIN_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    password2 = forms.CharField(label=_("Repeat password"), required=True, min_length=MIN_LENGTH, max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    
    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
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
    
    def save(self, commit=True):
        user = GeoUser(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        if commit:
            try:
                user.send_confirm_code()
                #Registration succesfully
                return user
            except NotSavedError, e:#new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
                fail = _('Email already in use')
                self._errors['email'] = self.error_class([fail])
            except Exception, e:#new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
                fail = _(e.message)
                self._errors['email'] = self.error_class([fail])


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}))


class UserForm(forms.Form):
    """
        Allow the user to change somo info of his account
    """
    created = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly':True}))
    email = forms.EmailField(required=True)
    old_pass = forms.CharField(label=_("Current password"), required=False,max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    password = forms.CharField(label=_("New password"), required=False,min_length=MIN_LENGTH, max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))
    password2 = forms.CharField(label=_("Repeat new password"), required=False,min_length=MIN_LENGTH, max_length=MAX_LENGTH, widget=forms.PasswordInput(attrs={'size':PWD_LENGTH}))

    
    def clean(self):
        """
         Clean data and check if the old pass is input and the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        old_pass = cleaned_data.get('old_pass')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password or password2:
            if old_pass:#to change password, user must write old pass first
                if password.find(' ') != -1:
                    msg = _("Passwords can't have white spaces")
                    self._errors['password'] = self.error_class([msg])
                elif password != password2:
                    msg = _("Passwords must be the same.")
                    self._errors['password'] = self.error_class([msg])
            else:
                msg = _("Old password needed.")
                self._errors['old_pass'] = self.error_class([msg])
            
        return cleaned_data 
                
    def save(self, user, commit=True):
        email = self.cleaned_data['email']
        old_pass = self.cleaned_data['old_pass']
        password = self.cleaned_data['password']
        
        if old_pass != "" and password != "":#user wants to change password
            if user.check_password(old_pass):
                user.password = password
            else:
                msg = _("Old password wrong.")
                self._errors['old_pass'] = self.error_class([msg])
                return None
        elif email != user.email:#user only wants to change the email
            user.email = email
                
        if commit:
            try:
                from georemindme.models import GeoUser
                user.put()
            except GeoUser.UniqueEmailConstraint:#email already in use
                msg = _("email already in use")
                self._errors['email'] = self.error_class([msg])
                return None
            except Exception:
                msg = _("A error ocurred, try again later")
                self._errors['email'] = self.error_class([msg])
                return None
           
        return user     

class LocationField(forms.Field):
    widget = LocationWidget

    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
            
        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)

class RemindForm(forms.Form):
    name = forms.CharField(required=True)
    location = LocationField(required=True)
    starts = forms.DateTimeField(required=False, widget=SelectDateWidget())
    ends = forms.DateTimeField(required=False, widget=SelectDateWidget())
    description = forms.CharField(required=False,widget=forms.Textarea())
    distance = forms.CharField(label=_('Alert distance (meters)'), required=False)
    active = forms.BooleanField(required=False, initial=True)
    done = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'done' in kwargs['initial']:#only shows done field when
                self.fields['done'] = forms.BooleanField() 
                
        elif 'done' in args[0]:
            self.fields['done'] = forms.BooleanField()

    def clean_distance(self):
        data = self.cleaned_data['distance']
        if data == '':
            return 0
        else:
            try:
                return int(float(data))#remove decimals
            except:
                raise forms.ValidationError(_('Distance must be a number'))
            
    def clean(self):
        cleaned_data = self.cleaned_data
        starts = cleaned_data.get('starts')
        ends = cleaned_data.get('ends')
        
        if all([starts, ends]):
            if (starts > ends):
                msg = _("Wrong dates")
                self._errors['starts'] = self.error_class([msg])
        
        return cleaned_data
    
    # only save if it is valid
    def save(self,**kwargs):
        lat, lng = self.cleaned_data['location'].split(',')
        if kwargs.get('id'):
            alert = Alert.objects.get_by_id_user(kwargs['id'], kwargs['user'])
            
            if not alert:
                return None
         
            alert.name = self.cleaned_data['name']
            alert.poi.name=self.cleaned_data['name']
            alert.poi.point=GeoPt(float(lat),float(lng))
            alert.poi.address=kwargs.get('address','')
            alert.poi.put()
        else:
            p = Point(name=self.cleaned_data['name'],point = GeoPt(float(lat),float(lng)),address=kwargs.get('address','') )
            p.put()
            alert = Alert(name=self.cleaned_data['name'],user=kwargs['user'],poi=p, done=True) # duck!
            
        alert.starts = self.cleaned_data['starts']
        alert.ends = self.cleaned_data['ends']
        alert.description = self.cleaned_data['description']
        
        alert.set_distance(self.cleaned_data['distance'])
        if not alert.is_active() == self.cleaned_data.get('active', False):
            alert.toggle_active()
        if not alert.is_done() == self.cleaned_data.get('done', False):
            alert.toggle_done()
            
        
        if kwargs.get("commit",True):
            alert.put()
        
        return alert
    
    def delete(self, **kwargs):
        if kwargs.get('id'):
            alert = Alert.objects.get_by_id_user(kwargs['id'], kwargs['user'])
            if not alert:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied()
            alert.delete()
            return True
        return False    
