# coding=utf-8

"""
.. module:: Forms
    :platform: appengine
    :synopsis: Formularios para recibir datos
"""

from django import forms
from django.utils.translation import gettext as _
from django.conf import settings


class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

class RecoverPassForm(forms.Form):
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repetir contraseña"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Las contraseñas no pueden contener espacios en blanco")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Las contraseñas deben coincidir.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data


class LoginForm(forms.Form):
    """
        Form for the login process
    """
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    remember_me = forms.BooleanField(label=_("Recordar contraseña?"), required=False,
                                     widget=forms.CheckboxInput(),
                                     initial = False
                                     )


class RegisterForm(forms.Form):
    """
        Form for the register process
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repetir contraseña"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Las contraseñas no pueden contener espacios en blanco")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Las contraseñas tienen que ser iguales.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data

    def save(self, language='en', commit=True):
        from models import User
        try:
            return User.register(email=self.cleaned_data['email'], password=self.cleaned_data['password'], language=language)
        except User.UniqueEmailConstraint, e:
            fail = _('Cuenta de correo en uso')
            self._errors['email'] = self.error_class([fail])
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            

class SocialTwitterUserForm(forms.Form):
    '''
        Formulario para pedir un correo y username a los usuarios que entran desde una red social
    '''
    email = forms.EmailField(label=_('email'), required=True)
    username = forms.CharField(label=_('username'), required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repetir contraseña"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    
    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Las contraseñas no pueden contener espacios en blanco")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Las contraseñas tienen que ser iguales.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data
    
    def save(self, user):
        from geouser.models import User
        try:
            result=  user.update(email=self.cleaned_data['email'], 
                                 username=self.cleaned_data['username'], 
                                 password=self.cleaned_data['password']
                                 )
        except User.UniqueEmailConstraint, e:
            fail = _('Cuenta de correo en uso')
            self._errors['email'] = self.error_class([fail])
            return
        except User.UniqueUsernameConstraint, e:
            fail = _('El nombre de usuario está siendo utilizado')
            self._errors['username'] = self.error_class([fail])
            return
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            return
        try: # usuario ya configurado, registramos como seguidor.
            generico = User.objects.get_by_username('georemindme')
            if generico is not None:
                user.add_following(followid=generico.id)
                generico.add_following(followid=user.id)
        except:
            pass
        return result
    
    
class SocialFacebookGoogleUserForm(forms.Form):
    '''
        Formulario para pedir un correo y username a los usuarios que entran desde una red social
    '''
    username = forms.CharField(label=_('nombre de usuario'), required=True)
    password = forms.CharField(required=True, max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repetir contraseña"), required=True,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    
    def clean(self):
        """
         Clean data and check if the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password.find(' ') != -1:
                msg = _("Las contraseñas no pueden contener espacios en blanco")
                self._errors['password'] = self.error_class([msg])

            if password != password2:
                msg = _("Las contraseñas tienen que ser iguales.")
                self._errors['password'] = self.error_class([msg])

        return cleaned_data
    
    def save(self, user):
        from geouser.models import User
        try:
            result =  user.update(username=self.cleaned_data['username'],
                                  password=self.cleaned_data['password']
                                  )
        except User.UniqueUsernameConstraint, e:
            fail = _('El nombre de usuario está siendo utilizado')
            self._errors['username'] = self.error_class([fail])
            return
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            return
        try: # usuario ya configurado, registramos como seguidor.
            generico = User.objects.get_by_username('georemindme')
            if generico is not None:
                user.add_following(followid=generico.id)
                generico.add_following(followid=user.id)
        except:
            pass
        return result
    
    
class SocialUserForm(forms.Form):
    '''
        Formulario para pedir un correo y username a los usuarios que entran desde una red social
    '''
    username = forms.CharField(label=_('nombre de usuario'), required=True)
    
    def save(self, user):
        from geouser.models import User
        try:
            result =  user.update(username=self.cleaned_data['username'])
        except User.UniqueUsernameConstraint, e:
            fail = _('El nombre de usuario está siendo utilizado')
            self._errors['username'] = self.error_class([fail])
            return
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            return
        try: # usuario ya configurado, registramos como seguidor.
            generico = User.objects.get_by_username('georemindme')
            if generico is not None:
                user.add_following(followid=generico.id)
                generico.add_following(followid=user.id)
        except:
            pass
        return result

AVATAR_CHOICES = (
          ('none', _('Nadie')),
          ('facebook', _('Facebook')),
          ('twitter', _('Twitter')),
          ('gravatar', _('Gravatar')),
                 )
class UserProfileForm(forms.Form):
    username = forms.CharField(label=_('nombre de usuario'), required=True)
    email = forms.EmailField(label=_('email'), required=True)
    description = forms.CharField(widget=forms.TextInput(), required=False)
    sync_avatar_with = forms.ChoiceField(label=_('Sincroniza tu avatar con'), choices=AVATAR_CHOICES)
    old_password = forms.CharField(label=_("Contraseña actual"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password = forms.CharField(label=_("Nueva contraseña"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repita la nueva contraseña"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    
    def clean(self):
        """
         Clean data and check if the old pass is input and the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        old_pass = cleaned_data.get('old_password')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password or password2:
            if old_pass:  # to change password, user must write old pass first
                if password.find(' ') != -1:
                    msg = _("Las contraseñas no pueden contener espacios en blanco")
                    self._errors['password'] = self.error_class([msg])
                elif password != password2:
                    msg = _("Las contraseñas tienen que ser iguales.")
                    self._errors['password'] = self.error_class([msg])
            else:
                msg = _("Necesita introducir la antigua contraseña.")
                self._errors['old_password'] = self.error_class([msg])
        return cleaned_data
    
    def save(self, user):
        from geouser.models import User
        try:
            if self.cleaned_data['password'] is not None:
                user.update(username=self.cleaned_data['username'], 
                            email=self.cleaned_data['email'], 
                            description=self.cleaned_data['description'], 
                            sync_avatar_with = self.cleaned_data['sync_avatar_with'],
                            password = self.cleaned_data['password'], 
                            old_password=self.cleaned_data['old_password'])
            else: 
                user.update(username=self.cleaned_data['username'], 
                            email=self.cleaned_data['email'], 
                            description=self.cleaned_data['description'], 
                            sync_avatar_with = self.cleaned_data['sync_avatar_with'])
            return user
        except User.UniqueEmailConstraint:  # Cuenta de correo en uso
            raise
            fail = _("Cuenta de correo en uso")
            self._errors['email'] = self.error_class([fail])
            return None
        except User.UniqueUsernameConstraint, e:
            raise
            fail = _('El nombre de usuario está siendo utilizado')
            self._errors['username'] = self.error_class([fail])
            return None
        except Exception, e:  # new user is not in DB so raise NotSavedError instead of UniqueEmailConstraint
            raise
            fail = _(e.message)
            self._errors['email'] = self.error_class([fail])
            return None


class UserForm(forms.Form):
    """
        Allow the user to change somo info of his account
    """
    email = forms.EmailField(required=True)
    old_pass = forms.CharField(label=_("Contraseña actual"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password = forms.CharField(label=_("Nueva contraseña"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )
    password2 = forms.CharField(label=_("Repita la nueva contraseña"), required=False,
                               max_length=settings.MAX_PWD_LENGTH,
                               min_length=settings.MIN_PWD_LENGTH,
                               widget=forms.PasswordInput(attrs={'size': settings.MAX_PWD_LENGTH+2})
                               )

    def clean(self):
        """
         Clean data and check if the old pass is input and the two passwords are the same
        """
        cleaned_data = self.cleaned_data
        old_pass = cleaned_data.get('old_pass')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password or password2:
            if old_pass:  # to change password, user must write old pass first
                if password.find(' ') != -1:
                    msg = _("Las contraseñas no pueden contener espacios en blanco")
                    self._errors['password'] = self.error_class([msg])
                elif password != password2:
                    msg = _("Las contraseñas tienen que ser iguales.")
                    self._errors['password'] = self.error_class([msg])
            else:
                msg = _("Necesita introducir la antigua contraseña.")
                self._errors['old_pass'] = self.error_class([msg])
        return cleaned_data

    def save(self, user, commit=True):
        from geouser.models import User
        email = self.cleaned_data['email']
        old_pass = self.cleaned_data['old_pass']
        password = self.cleaned_data['password']

        if old_pass != "" and password != "":  # user wants to change password
            if user.check_password(old_pass):
                user.password = password
            else:
                msg = _("La antigua contraseña es incorrecta.")
                self._errors['old_pass'] = self.error_class([msg])
                return None
        elif email != user.email:  # user only wants to change the email
            user.email = email

        if commit:
            try:
                user.put()
            except User.UniqueEmailConstraint:  # Cuenta de correo en uso
                msg = _("Cuenta de correo en uso")
                self._errors['email'] = self.error_class([msg])
                return None
            except Exception:
                msg = _("A error ocurred, try again later")
                self._errors['email'] = self.error_class([msg])
                return None

        return user


CHOICES = (
           ('never', _('Nunca')),
           ('instant', _('Instantáneamente')),
           ('daily', _('Diario')),
           ('weekly', _('Semanal')),
           ('monthly', _('Mensual')),
           )
class UserSettingsForm(forms.Form):
    show_public_profile = forms.BooleanField(label=_('Visibilidad del perfil'), required=False)
    time_notification_suggestion_follower = forms.ChoiceField(label=_('Nuevo seguidor en una sugerencia'), choices=CHOICES)
    time_notification_suggestion_comment = forms.ChoiceField(label=_('Nuevo comentario en una sugerencia'), choices=CHOICES)
    time_notification_account = forms.ChoiceField(label=_('Nuevo seguidor de la cuenta'), choices=CHOICES)
    language = forms.ChoiceField(label=_('Idioma'), choices=settings.LANGUAGES, required=False)
    
    
    def save(self, user):
        try:
            user.settings.show_public_profile = self.cleaned_data['show_public_profile']
            user.settings.time_notification_suggestion_follower = self.cleaned_data['time_notification_suggestion_follower']
            user.settings.time_notification_suggestion_comment = self.cleaned_data['time_notification_suggestion_comment']
            user.settings.time_notification_account = self.cleaned_data['time_notification_account']
            user.settings.language = self.cleaned_data['language']
            user.settings.put()
        except:
            raise
            return False
