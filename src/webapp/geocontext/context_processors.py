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
from geouser.models import AnonymousUser
from georemindme.forms import ContactForm
from django.conf import settings
from string import find

def geoAuth(request):
    """
        Add the object user to all templates
    """
    parameters = {
            'user' : request.user,
            'contactForm' : ContactForm(),
            'app_settings' :{
                                u'appId': settings.OAUTH['facebook']['app_key'],
                                u'canvasName': settings.FACEBOOK_APP['canvas_name'],
                            },
            'notifications': request.user.counters.notifications if request.user.is_authenticated() else None,
            'in_facebook': True if request.path.find('/fb/') == 0 else False,
            }
    return parameters
    
        
    
        
