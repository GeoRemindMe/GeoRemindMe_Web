# coding=utf-8

import facebook
import simplejson

from google.appengine.ext import db
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


from settings import OAUTH, FACEBOOK_APP

FACEBOOK_APP_ID = OAUTH['facebook']['app_key']
FACEBOOK_APP_SECRET = OAUTH['facebook']['app_secret']

class User2(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)


"""Provides access to the active Facebook User2 in self.current_user

The property is lazy-loaded on first access, using the cookie saved
by the Facebook JavaScript SDK to determine the User2 ID of the active
User2. See http://developers.facebook.com/docs/authentication/ for
more information.
"""
#~ @property
@csrf_exempt
def login_panel(request):
    if not "current_user" in request.session or request.session["current_user"]==None:
        request.session["current_user"] = None
        cookie = facebook.get_user_from_cookie(
            request.COOKIES, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        
        
        if cookie:

            user = User2.get_by_key_name(cookie["uid"])
            if not user:
                graph = facebook.GraphAPI(cookie["access_token"])
                profile = graph.get_object("me")
                user = User2(key_name=str(profile["id"]),
                            id=str(profile["id"]),
                            name=profile["name"],
                            profile_url=profile["link"],
                            access_token=cookie["access_token"])
                user.put()
            elif user.access_token != cookie["access_token"]:
                user.access_token = cookie["access_token"]
                user.put()
        
    
    graph = facebook.GraphAPI("102408026518300|3740790edde68dc4c281a6c2.1-100002508846747|Nq7_aAjY4P9dNAuGEEwKKOc0AG4")
    profile = graph.get_object("me")
    user = User2(key_name=str(profile["id"]),
                id=str(profile["id"]),
                name=profile["name"],
                profile_url=profile["link"],
                access_token="102408026518300|3740790edde68dc4c281a6c2.1-100002508846747|Nq7_aAjY4P9dNAuGEEwKKOc0AG4")
                
    args = dict(current_user=user,
                facebook_app_id=FACEBOOK_APP_ID)
    
    return  render_to_response('example.html',args)


