# coding=utf-8


from django import forms
from django.utils.translation import ugettext as _


from georemindme.models_utils import VISIBILITY_CHOICES


class ListRequestedForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False,widget=forms.Textarea())    
    visibility = forms.ChoiceField(required=True, choices=VISIBILITY_CHOICES)
    
    # only save if it is valid
    def save(self, **kwargs):
        from geouser.models import User
        if not isinstance(kwargs['user'], User):
            raise TypeError
        from models import ListRequested
        if kwargs['id'] is None:
            list = ListRequested.insert_list(user=kwargs['user'],
                                             name=self.cleaned_data['name'],
                                             description=self.cleaned_data['description']
                                             )