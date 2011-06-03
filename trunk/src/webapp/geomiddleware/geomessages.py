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

#===============================================================================
# http://www.cupcakewithsprinkles.com/django-messaging-for-ajax-calls-using-jquery/
#===============================================================================

from django.utils import simplejson
from django.contrib import messages

class AJAXMessage(object):
    def process_response(self, request, response):
        if all([request.is_ajax(), response['Content-Type'] in ["application/javascript", "application/json"]]):
            try:
                content = dict(simplejson.loads(response.content))
            except:
                return response
            
            sys_messages = []
            for message in messages.get_messages(request):
                sys_messages.append({
                                        'level': message.level,
                                        'message': message.message,
                                        'extra_tags': message.tags
                                        })
            if len(sys_messages) != 0:
                content['sys_messages'] = sys_messages
                response.content = simplejson.dumps(content)
        return response
                
        