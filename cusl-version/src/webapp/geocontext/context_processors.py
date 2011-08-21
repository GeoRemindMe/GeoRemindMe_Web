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

class AnonymousUser(object):
    email = ''
    active = False
   
    def is_authenticated(self):
        return False
    
    def is_admin(self):
        return False

def geoAuth(request):
    """
        Add the object user to all templates
    """
    from georemindme.forms import ContactForm
    return {
            'user' : request.session.get('user', AnonymousUser()), #user is authenticated
            'contactForm' : ContactForm(),
            }
    
        
    
        