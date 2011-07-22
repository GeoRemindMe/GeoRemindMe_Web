# coding=utf-8


from django.shortcuts import render_to_response, Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import decorator_from_middleware
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from geouser.models import *
from geouser.funcs import init_user_session
from geoalert.models import *
from decorators import facebook_required


def login_panel(request):
    from geouser.forms import SocialUserForm
    if hasattr(request, 'facebook'):
        if not request.user.is_authenticated():
            user = request.facebook['client'].authenticate()
            init_user_session(request, user, is_from_facebook=True)

        else:
            user = request.user
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
        else:
            return HttpResponseRedirect(reverse('facebookApp.views.dashboard'))
    #Identificarse o registrarse
    return render_to_response('register.html', {"permissions":settings.OAUTH['facebook']['scope']}, context_instance=RequestContext(request))
    

@facebook_required
def dashboard(request):
    friends_to_follow=request.user.get_friends_to_follow()
    followers=request.user.get_followers()
    followings=request.user.get_followings()
    chronology = request.user.get_chronology()
    timeline = request.user.get_timelineALL()
    chronology[1].extend(timeline[1])
    chronology[1].sort(key=lambda x: x['modified'], reverse=True)
    return  render_to_response('dashboard.html', {'friends_to_follow': friends_to_follow,
                                                  'followers': followers,
                                                  'followings': followings, 
                                                  'chronology': chronology,
                                                  } , RequestContext(request))


@facebook_required
def profile(request, username):
    """**Descripción**: Perfil publico que veran los demas usuarios
    
    :param username: nombre de usuario
    :type username: ni idea
    """
    
    if request.user.username.lower() == username.lower():
        # Si el usuario esta viendo su propio perfil
        profile = request.user.profile
        counters = request.user.counters_async()
        sociallinks = profile.sociallinks_async()
        timeline = UserTimeline.objects.get_by_id(request.user.id)
        is_following = True
        is_follower = True
        show_followers = True
        show_followings = True
    else:
        # Si esta viendo el perfil de otro
        profile_user = User.objects.get_by_username(username)
        if profile_user is None:
            raise Http404()
        counters = profile_user.counters_async()#UserCounter.objects.get_by_id(profile_user.id, async=True)
        
        settings = profile_user.settings
        profile = profile_user.profile
        sociallinks = profile.sociallinks_async()
        
        if request.user.is_authenticated():
            is_following = profile_user.is_following(request.user)
            is_follower = request.user.is_following(profile_user)
        else:
            is_following = None
            is_follower = None
        if is_following:  # el usuario logueado, sigue al del perfil
            timeline = UserTimeline.objects.get_by_id(profile_user.id, querier=request.user)
        elif settings.show_timeline:
            timeline = UserTimeline.objects.get_by_id(profile_user.id)
        show_followers = settings.show_followers,
        show_followings = settings.show_followings
    
    return render_to_response('profile.html', {'profile': profile, 
                                                'counters': counters.next(),
                                                'sociallinks': sociallinks.next(),
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
            if modified:
                return HttpResponseRedirect('/fb/user/%s/' % request.user.username)

    else:
        f = UserProfileForm(initial={'username': request.user.username,
                                     'email': request.user.email,
                                     'description': request.user.profile.description, 
                                     'sync_avatar_with': request.user.profile.sync_avatar_with, },
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
    from geoalert.views import get_suggestion
    counters = request.user.counters_async()
    suggestions = get_suggestion(request, id=None,
                                wanted_user=request.user,
                                private_profile=True,
                                page = 1, query_id = None
                                )
    return  render_to_response('suggestions.html',{'suggestions': suggestions,
                                                   'counters': counters.next()}, context_instance=RequestContext(request))


@facebook_required    
def add_suggestion(request):
    from geoalert.forms import SuggestionForm
    f = SuggestionForm();

    return  render_to_response('add_suggestion.html',{'f': f,}, context_instance=RequestContext(request))
    

@facebook_required    
def edit_suggestion(request,suggestion_id):
    from geoalert.forms import SuggestionForm
    s = Suggestion.objects.get_by_id(suggestion_id)
    return  render_to_response('add_suggestion.html', {
                                                        
                                                        'eventid':suggestion_id,
                                                        'name': s.name,
                                                        'poi_id': s.poi.id,
                                                        'poi_reference': s.poi.google_places_reference,
                                                        'starts': s.date_starts,
                                                        'ends': s.date_ends,
                                                        'description': s.description, 
                                                        'visibility': s._vis,
                                                        'poi_location': s.poi.location,
                                                        'poi_name': s.poi.name,
                                                        'poi_address': s.poi.address,
                                                        }, context_instance=RequestContext(request)
                               )
@facebook_required
def view_suggestion(request,suggestion_id):
    from geoalert.views import suggestion_profile
    return suggestion_profile(request, suggestion_id, template='view_suggestion.html')
    


@facebook_required
def view_place(request, place_id):
    from geoalert.views import view_place
    return view_place(request, place_id, template='view_place.html')


@facebook_required
def profile_settings(request):
    counters = request.user.counters_async()
    has_twitter = True if request.user.twitter_user is not None else False
    has_google = True if request.user.google_user is not None else False
    
    return  render_to_response('settings.html',{'counters': counters.next(),
                                               'profile': request.user.profile,
                                               'has_twitter': has_twitter,
                                               'has_google': has_google,
                                               'settings': request.user.settings,
                                                }, context_instance=RequestContext(request))
   

@facebook_required
def edit_settings(request):
    from geouser.forms import UserSettingsForm
    if request.method == 'POST':
        f = UserSettingsForm(request.POST, prefix='user_set_settings')
        if f.is_valid():
            f.save(request.user)
            request.session['LANGUAGE_CODE'] = request.user.settings.language
            return HttpResponseRedirect(reverse('facebookApp.views.profile_settings'))
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
    
