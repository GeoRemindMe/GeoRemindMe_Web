# coding=utf-8


from django.shortcuts import render_to_response, Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global

from geouser.funcs import init_user_session
from decorators import facebook_required


def login_panel(request):
    from geouser.forms import SocialUserForm
    if hasattr(request, 'facebook'):
        if not request.user.is_authenticated():
            user = request.facebook['client'].authenticate()
            if not user:
                return render_to_response('register.html', {"permissions": __web_settings.OAUTH['facebook']['scope'] },
                              context_instance=RequestContext(request)
                              )
            # ya conociamos al usuario
            init_user_session(request, user, remember=True, is_from_facebook=True)
            request.user = user
        if request.user.is_authenticated():
            if request.user.username is None or request.user.email is None:
                if request.method == 'POST':
                    f = SocialUserForm(request.POST, 
                                       prefix='user_set_username', 
                                       initial = { 'email': request.user.email,
                                                   'username': request.user.username,
                                                 }
                                       )
                    if f.is_valid():
                        user = f.save(request.user)
                        if user:
                            init_user_session(request, user, remember=True, is_from_facebook=True)
                            return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
                else:
                    f = SocialUserForm(prefix='user_set_username', 
                                       initial = { 'email': request.user.email,
                                                   'username': request.user.username,
                                                  }
                                       )
                return render_to_response('create_social_profile.html', {'form': f}, 
                                           context_instance=RequestContext(request)
                                          )
            else: # setup del usuario completo
                if request.facebook['client'].user is None:
                    try:
                        request.facebook['client'].authorize(request.user)
                        init_user_session(request, request.user, remember=True, is_from_facebook=True)
                    except:
                        return render_to_response('register.html', {'permissions': __web_settings.OAUTH['facebook']['scope'] },
                                                context_instance=RequestContext(request)
                              )
                return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
    #Identificarse o registrarse
    return render_to_response('register.html', {'permissions': __web_settings.OAUTH['facebook']['scope'] },
                                                context_instance=RequestContext(request)
                              )
    

@facebook_required
def dashboard(request):
    if request.user.username is None or request.user.email is None:
        return HttpResponseRedirect('fb_login_panel')
    from geouser.views import dashboard
    return dashboard(request, template='dashboard.html')

         
@facebook_required
def notifications(request):
    from geouser.views import notifications
    return notifications(request, template='notifications.html')


@facebook_required
def profile(request, username):
    from geouser.views import public_profile
    return public_profile(request, username, template='profile.html')


@facebook_required
def edit_profile (request):
    from geouser.views import edit_profile
    return edit_profile(request, template='edit_profile.html')


@facebook_required    
def user_suggestions(request):
    from geoalert.views import user_suggestions
    return user_suggestions(request, template='suggestions.html')


@facebook_required    
def search_suggestions(request,term=None):
    from georemindme.views import search_suggestions
    return search_suggestions(request, term, template='search.html')    


@facebook_required    
def add_suggestion(request):
    from geoalert.views import add_suggestion
    return add_suggestion(request, template='add_suggestion.html')
    

@facebook_required    
def edit_suggestion(request, suggestion_id):
    from geoalert.views import edit_suggestion
    return edit_suggestion(request, suggestion_id, template='add_suggestion.html')


@facebook_required
def view_suggestion(request, slug):
    from geoalert.views import suggestion_profile
    return suggestion_profile(request, slug, template='view_suggestion.html')


@facebook_required
def view_list(request, id):
    from geolist.views import view_list
    return view_list(request, id, template='view_list.html')


@facebook_required
def view_place(request, place_id):
    from geoalert.views import view_place
    return view_place(request, place_id, template='view_place.html')


@facebook_required
def view_tag_suggestions(request, slug):
    from geotags.views import view_tag_suggestions
    return view_tag_suggestions(request, slug, template='view_tag.html')


@facebook_required
def profile_settings(request):
    from geouser.views import profile_settings
    return profile_settings(request, template='settings.html')
   

@facebook_required
def edit_settings(request):
    from geouser.views import edit_settings
    return edit_settings(request, template="edit_settings.html")


@facebook_required
def followers_panel(request, username):
    from geouser.views import followers_panel
    return followers_panel(request, username, template='followers.html')


@facebook_required
def followings_panel(request, username):
    from geouser.views import followings_panel
    return followings_panel(request, username, template='followings.html')


def test_users(request):
    from geoauth.clients.facebook import add_test_users
    user = add_test_users()
    return HttpResponse(user)


def get_test_users(request):
    from geoauth.clients.facebook import get_test_users
    user = get_test_users()
    return HttpResponse(user)
