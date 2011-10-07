# coding=utf-8

"""
.. module:: forms
    :platform: appengine
    :synopsis: Formularios comunes para todo el proyecto
"""


from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label=_('Name'))
    email = forms.EmailField(required=True, label=_('Email'))
    message = forms.CharField(label=_('Mensaje'), required=True,
                              widget=forms.Textarea(attrs={'cols': 10, 'rows': 10})
                              )
