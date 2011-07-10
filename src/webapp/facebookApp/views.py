# coding=utf-8


from django.shortcuts import render_to_response, Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import decorator_from_middleware
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from geouser.models import *
from geouser.forms import *
from geouser.funcs import init_user_session
from geoalert.forms import *
from geoauth.clients.facebook import *
from decorators import facebook_required


def login_panel(request):
    if hasattr(request, 'facebook'):
        user = request.facebook['client'].authenticate()
        init_user_session(request, user, is_from_facebook=True)
        if user.username is None or user.email is None:
                if request.method == 'POST':
                    f = SocialUserForm(request.POST, prefix='user_set_username', initial = { 
                                                                          'email': user.email,
                                                                          'username': user.username,
                                                                          })
                    if f.is_valid():
                        user = f.save(user)
                        if user:
                            request.user = user
                            return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
                else:
                    f = SocialUserForm(prefix='user_set_username', initial = { 
                                                                          'email': request.user.email,
                                                                          'username': request.user.username,
                                                                          })
                
                return render_to_response('create_social_profile.html', {'form': f}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
        
    #Identificarse o registrarse
    return render_to_response('register.html', {"permissions":settings.OAUTH['facebook']['scope']}, context_instance=RequestContext(request))
    


@facebook_required
def dashboard(request):
    friends_to_follow=request.facebook['client'].get_friends_to_follow()    
    followers=request.user.get_followers()
    followings=request.user.get_followings()
    
    return  render_to_response('dashboard.html', {'friends_to_follow': friends_to_follow,
                                                  'followers': followers,
                                                  'followings': followings, 
                                                  } , RequestContext(request))


@facebook_required
def public_profile(request, username):
    """**Descripción**: Perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    
    if request.user.username.lower() == username.lower():
        profile = request.user.profile
        timeline = UserTimeline.objects.get_by_id(request.user.id)
        is_following = True
        is_follower = True
        counters = request.user.counters
        show_followers = True
        show_followings = True
    else:
        profile_user = User.objects.get_by_username(username)
        if profile_user is None:
            raise Http404()
        settings = profile_user.settings
        profile = profile_user.profile
        counters = UserCounter.objects.get_by_id(profile_user.id, async=True)
        if request.user.is_authenticated():
            is_following = profile_user.is_following(request.user)
            is_follower = request.user.is_following(profile_user)
        else:
            is_following = None
            is_follower = None
        if is_following:  # el usuario logueado, sigue al del perfil
            timeline = UserTimeline.objects.get_by_id(profile_user.id, vis='shared')
        elif settings.show_timeline:
            timeline = UserTimeline.objects.get_by_id(profile_user.id)
        counters.get_result()
        show_followers = settings.show_followers,
        show_followings = settings.show_followings
    return render_to_response('profile.html', {'profile': profile, 
                                                'counters': counters,
                                                'timeline': timeline, 
                                                'is_following': is_following,
                                                'is_follower': is_follower, 
                                                'show_followers': show_followers,
                                                'show_followings': show_followings
                                                }, context_instance=RequestContext(request))


@facebook_required
def edit_profile (request):
    """**Descripción**: Edición del perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    from geouser.forms import UserProfileForm
    if request.method == 'POST':
        f = UserProfileForm(request.POST, prefix='user_set_profile')
        if f.is_valid():
            modified = f.save(user=request.user)
    else:
        f = UserProfileForm(initial={'username': request.user.username,
                                     'email': request.user.email,
                                     'description': request.user.profile.description, },
                            prefix='user_set_profile'
                            )
    #~ raise Exception(f)
    return render_to_response('edit_profile.html', {'form': f}, context_instance=RequestContext(request))

@facebook_required    
def user_suggestions(request):
    """
    name = forms.CharField(required=True)
    location = LocationField(required=True)
    poi_id = forms.IntegerField(required=False, initial=-1)
    starts = forms.DateTimeField(required=False, widget=SelectDateWidget())
    ends = forms.DateTimeField(required=False, widget=SelectDateWidget())
    description = forms.CharField(required=False,widget=forms.Textarea())
    distance = forms.CharField(label=_('Alert distance (meters)'), required=False)
    active = forms.BooleanField(required=False, initial=True)
    done = forms.BooleanField(required=False)
    """
    f = RemindForm(initial = { 
                              # 'location' : [1,2] <<- coordenadas por defecto,
                              'name': 'Recomiendo...',
                              'done': False,
                              })
    return  render_to_response('suggestions.html',{'form': f}, context_instance=RequestContext(request))

@facebook_required    
def add_suggestion(request):
    f = SuggestionForm();
    #~ initial = { 
                              #~ # 'location' : [1,2] <<- coordenadas por defecto,
                              #~ 'name': 'Recomiendo...',
                              #~ 'done': False,
                              #~ })
    return  render_to_response('add_suggestion.html',{'f': f}, context_instance=RequestContext(request))

@facebook_required
def profile_settings(request):
    has_twitter = True if request.user.twitter_user is not None else False
    has_google = True if request.user.google_user is not None else False
    
    return  render_to_response('settings.html',{'counters': request.user.counters,
                                               'profile': request.user.profile,
                                               'has_twitter': has_twitter,
                                               'has_google': has_google,
                                               'settings': request.user.settings,
                                                }, context_instance=RequestContext(request))
@facebook_required
def edit_settings(request):
    if request.method == 'POST':
        
            
        f = UserSettingsForm(request.POST, prefix='user_set_settings', initial = { 
                                                                                  'time_notification_suggestion_follower': request.user.settings.time_notification_suggestion_follower,
                                                                                  'time_notification_suggestion_comment': request.user.settings.time_notification_suggestion_comment,
                                                                                  'time_notification_account': request.user.settings.time_notification_account,
                                                                                  'show_public_profile': request.user.settings.show_public_profile,
                                                                                  'language': request.user.settings.language,
                                                                                  })
        if f.is_valid():
            f.save(request.user)

    else:
        
        f = UserSettingsForm(prefix='user_set_settings', initial = { 
                                                                  'time_notification_suggestion_follower': request.user.settings.time_notification_suggestion_follower,
                                                                  'time_notification_suggestion_comment': request.user.settings.time_notification_suggestion_comment,
                                                                  'time_notification_account': request.user.settings.time_notification_account,
                                                                  'show_public_profile': request.user.settings.show_public_profile,
                                                                  'language': request.user.settings.language,
                                                                  })
	
    return  render_to_response('edit_settings.html',{'profile': request.user.profile,
                                                    'settings': request.user.settings,
                                                    'settings_form': f,
                                                    }, context_instance=RequestContext(request))

@facebook_required
def followers_panel(request, username):
    if username == request.user.username:
        followers=request.user.get_followers()
    else:
        user=User.objects.get_by_username(username)
        if user is None:
            raise Http404
        if user.settings.show_followers:
            followers = user.get_followers()
        else:
            followers = None
    return  render_to_response('followers.html', {'followers': followers[1],'username_page':username}, context_instance=RequestContext(request))


@facebook_required
def followings_panel(request, username):
    if username == request.user.username:
        followings=request.user.get_followings()
        user=request.user
    else:
        user = User.objects.get_by_username(username)
        #~ raise Exception("Entramos con ", username)
        if user is None:
            raise Http404
        if user.settings.show_followings:
            followings = user.get_followings()
        else:
            followings = None
    
    return  render_to_response('followings.html', {'followings': followings[1],'username_page':username}, context_instance=RequestContext(request))


def test_users(request):
    from geoauth.clients.facebook import add_test_users
    user = add_test_users()
    return HttpResponse(user)

def get_test_users(request):
    from geoauth.clients.facebook import get_test_users
    user = get_test_users()
    return HttpResponse(user)
    
