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
    starts = forms.SplitDateTimeField(required=False)
    ends = forms.SplitDateTimeField(required=False)
    description = forms.CharField(required=False,widget=forms.Textarea())
    distance = forms.CharField(label=_('Alert distance (meters)'), required=False)
    active = forms.BooleanField(required=False, initial=True)
    done = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            if 'done' in kwargs['initial']:#only shows done field when
                self.fields['done'] = forms.BooleanField() 
                
        elif args:
            if 'done' in args[0]:
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
                                         location = GeoPt(float(lat), float(long)),
                                         address = kwargs.get('address', ''),
                                         user = kwargs['user'])
        alert = Alert.update_or_insert(
                         id = kwargs.get('id', None), name = self.cleaned_data['name'],
                         description = self.cleaned_data['description'], 
                         date_starts = self.cleaned_data['starts'],
                         date_ends = self.cleaned_data['ends'], poi = poi,
                         user = kwargs['user'], done = self.cleaned_data.get('done', False),
                         active = None  # self.cleaned_data.get('active', True)
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

from georemindme.models_utils import VISIBILITY_CHOICES

class SuggestionForm(forms.Form):
    name = forms.CharField(required=True)
    poi_id = forms.IntegerField(required=False)
    place_reference = forms.CharField(required=False)
    starts_year = forms.IntegerField(required=False)
    starts_month = forms.IntegerField(required=False)
    starts_day = forms.IntegerField(required=False)
    ends_year = forms.IntegerField(required=False)
    ends_month = forms.IntegerField(required=False)
    ends_day = forms.IntegerField(required=False)
    starts_hour = forms.CharField(required=False)
    ends_hour = forms.CharField(required=False)
    description = forms.CharField(required=False,widget=forms.Textarea())
    tags = forms.CharField(required=False)    
    done = forms.BooleanField(required=False)
    visibility = forms.ChoiceField(required=False, choices=VISIBILITY_CHOICES)
    to_facebook = forms.BooleanField(required=False)
    to_twitter = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'done' in kwargs['initial']:#only shows done field when
                self.fields['done'] = forms.BooleanField() 
        elif args:
            if 'done' in args[0]:
                self.fields['done'] = forms.BooleanField()
            
    def clean(self):
        import datetime
        cleaned_data = self.cleaned_data
        try:
            starts = datetime.date(cleaned_data.get('starts_year', 1),
                                  cleaned_data.get('starts_month', 1),
                                  cleaned_data.get('starts_day', 1)
                                  )
            if starts != datetime.date(1,1,1):
                ends = datetime.date(cleaned_data.get('ends_year', 1),
                                  cleaned_data.get('ends_month', 1),
                                  cleaned_data.get('ends_day', 1)
                                 )
                if all([starts, ends]):
                    if (starts > ends):
                        msg = _("Wrong dates")
                        self._errors['starts'] = self.error_class([msg])
        except:
            pass
        return cleaned_data
    
    # only save if it is valid
    def save(self, list_id='', **kwargs):
        import datetime
        try:
            starts = datetime.date(self.cleaned_data.get('starts_year', 1),
                                   self.cleaned_data.get('starts_month', 1),
                                   self.cleaned_data.get('starts_day', 1)
                                   )
        except:
            starts = None
        try:
            ends = datetime.date(self.cleaned_data.get('ends_year', 1),
                              self.cleaned_data.get('ends_month', 1),
                              self.cleaned_data.get('ends_day', 1)
                             )
        except:
            ends = None
            
        import time
        time_format = "%H:%M"
        try:
            sh = time.strptime(self.cleaned_data['starts_hour'], time_format)
            starts_hour = datetime.time(sh[3], sh[4])
        except:
            starts_hour = None
        try:
            eh = time.strptime(self.cleaned_data['ends_hour'], time_format)
            ends_hour = datetime.time(eh[3], eh[4])
        except:
            ends_hour = None
        
        from geoalert.models import Suggestion
        if 'poi_id' in self.cleaned_data and self.cleaned_data['poi_id'] is not None:
            poi = Place.objects.get_by_id(self.cleaned_data['poi_id'])
            if poi is None:
                return None
        elif 'place_reference' in self.cleaned_data and self.cleaned_data['place_reference'] != '':
            poi = Place.insert_or_update_google(user=kwargs['user'],
                                                google_places_reference=self.cleaned_data['place_reference']
                                                )
            if poi is None:
                return None
        else:
            poi = None
        id = kwargs.get('id', None)
        try:
            suggestion = Suggestion.update_or_insert(
                     id = kwargs.get('id', None), name = self.cleaned_data['name'],
                     description = self.cleaned_data['description'], 
                     date_starts = starts,
                     date_ends = ends,
                     hour_starts = starts_hour,
                     hour_ends = ends_hour,
                     poi = poi,
                     user = kwargs['user'], done = self.cleaned_data.get('done', False),
                     tags = self.cleaned_data.get('tags', None),
                     vis = self.cleaned_data['visibility'],
                     to_facebook = self.cleaned_data['to_facebook'],
                     to_twitter = self.cleaned_data['to_twitter'],
                     )
        except:
            return None
        if suggestion is not None:
            list_id = list_id
            if list_id != '':
                ids = list_id.split(',')
                ids = filter(lambda x: x!='', ids)
                from geolist.models import ListSuggestion
                for list in ids:
                    ListSuggestion.insert_list(user=kwargs['user'],
                                                id=list, 
                                                instances=[suggestion.id]
                                                )
        return suggestion  
