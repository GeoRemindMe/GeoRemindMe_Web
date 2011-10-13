# coding=utf-8

from geouser.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def login_panel(request, login=False):
    try:
    # When deployed
        from google.appengine.runtime import DeadlineExceededError
    except ImportError:
    # In the development server
        from google.appengine.runtime.apiproxy_errors import DeadlineExceededError 
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mobileApp.views.dashboard'))
        return render_to_response("mobile/login.html", {'login' :login}, context_instance=RequestContext(request))
    except DeadlineExceededError:
        return HttpResponseRedirect('/m/')
    

@login_required
def dashboard(request):
    from geouser.views import dashboard
    return dashboard(request, template='mobile/dashboard.html')


@login_required         
def notifications(request):
    from geouser.views import notifications
    return notifications(request, template='mobile/notifications.html')


@login_required
def profile(request, username):
    from geouser.views import public_profile
    return public_profile(request, username, template='mobile/profile.html')


@login_required
def edit_profile (request):
    from geouser.views import edit_profile
    return edit_profile(request, template='mobile/edit_profile.html')


@login_required
def user_suggestions(request):
    from geoalert.views import user_suggestions
    return user_suggestions(request, template='mobile/suggestions.html')


@login_required
def search_suggestions(request,term=None):
    from georemindme.views import search_suggestions
    return search_suggestions(request, term, template='mobile/search.html')    


@login_required
def add_suggestion(request):
    from geoalert.views import add_suggestion
    return add_suggestion(request, template='mobile/add_suggestion.html')
    
 
@login_required
def edit_suggestion(request, suggestion_id):
    from geoalert.views import edit_suggestion
    return edit_suggestion(request, suggestion_id, template='mobile/add_suggestion.html')


@login_required
def view_suggestion(request, slug):
    from geoalert.views import suggestion_profile
    return suggestion_profile(request, slug, template='mobile/view_suggestion.html')


@login_required
def view_list(request, id):
    from geolist.views import view_list
    return view_list(request, id, template='mobile/view_list.html')


@login_required
def view_place(request, place_id):
    from geoalert.views import view_place
    return view_place(request, place_id, template='mobile/view_place.html')


@login_required
def view_tag_suggestions(request, slug):
    from geotags.views import view_tag_suggestions
    return view_tag_suggestions(request, slug, template='mobile/view_tag.html')


@login_required
def profile_settings(request):
    from geouser.views import profile_settings
    return profile_settings(request, template='mobile/settings.html')
   

@login_required
def edit_settings(request):
    from geouser.views import edit_settings
    return edit_settings(request, template="mobile/edit_settings.html")


@login_required
def followers_panel(request, username):
    from geouser.views import followers_panel
    return followers_panel(request, username, template='mobile/followers.html')


@login_required
def followings_panel(request, username):
    from geouser.views import followings_panel
    return followings_panel(request, username, template='mobile/followings.html')
