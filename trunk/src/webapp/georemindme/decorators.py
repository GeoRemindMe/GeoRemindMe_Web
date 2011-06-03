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
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from google.appengine.api import users
from appengine_utilities.sessions import Session

from models import User
"""
   login_required decorator
   
   It is used to check if a user is logged in or not    
"""
def login_required(func):
    def _wrapper(*args, **kwargs):
        session = args[0].session#request es el primer parametro que pasamos
        user = session.get('user')
        if user and user.is_authenticated():
            return func(*args, **kwargs)
        user = users.get_current_user()
        if user:#user is from google
            u = User.objects.get_by_google_id(user.user_id())
            if u and u.is_authenticated():
                if u.is_authenticated():
                    u._session = session.get_ds_entity()
                    session['user'] = u
                    return func(*args, **kwargs)
        return HttpResponseRedirect('/login/')
    return _wrapper

def ajax_request(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        if request.method <> "POST" or not request.is_ajax():
            return HttpResponseBadRequest("Not AJAX or POST", mimetype="text/plain")
        return func(*args, **kwargs)
    return _wrapper