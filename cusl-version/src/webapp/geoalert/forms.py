# coding=utf-8


from django import forms
from django.utils.translation import ugettext as _
from django.forms.extras.widgets import SelectDateWidget

from google.appengine.ext.db import GeoPt, NotSavedError

from models import Alert
from models_poi import *
from geouser.models import User
from widgets import LocationWidget

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
    poi_id = forms.IntegerField(required=False, initial=-1)
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
    def save(self, **kwargs):
        lat, long = self.cleaned_data['location'].split(',')
        poi = PrivatePlace.get_or_insert(id = self.cleaned_data['poi_id'],
                                         name = '',
                                         point = GeoPt(float(lat), float(long)),
                                         address = kwargs.get('address', ''),)
        alert = Alert.update_or_insert(
                         id = kwargs.get('id', None), name = self.cleaned_data['name'],
                         description = self.cleaned_data['description'], 
                         date_starts = self.cleaned_data['starts'],
                         date_ends = self.cleaned_data['ends'], poi = poi,
                         user = kwargs['user'], done = self.cleaned_data.get('done', False),
                         active = self.cleaned_data.get('active', False)
                         )
        
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
