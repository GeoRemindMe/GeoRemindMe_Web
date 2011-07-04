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
        if request.user.is_authenticated():  # usuario identificado y con permisos
            if request.user.username is None or request.user.email is None:
                if request.method == 'POST':
                    f = SocialUserForm(request.POST, prefix='user_set_username')
                    if f.is_valid():
                        user = f.save(request.user)
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
        else:  # tenemos permisos pero no sabemos que usuario es, por tanto, autenticarlo e iniciar sesion
            user = request.facebook['client'].authenticate()
            init_user_session(request, user)
            #Renderizamos de nuevo esta plantilla para que le pida usuario y mail
            return HttpResponseRedirect(reverse('facebookApp.views.login_panel'))
    #Identificarse o registrarse
    return render_to_response('register.html', {"permissions":settings.OAUTH['facebook']['scope']}, RequestContext(request))
    


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
    profile_user = User.objects.get_by_username(username)
    if profile_user is None:
        raise Http404()
    settings = profile_user.settings
    profile = profile_user.profile
    counters = UserCounter.objects.get_by_id(profile_user.id, async=True)
    if request.user.id == profile_user.id:
        if settings.show_timeline:
            timeline = UserTimeline.objects.get_by_id(profile_user.id)
            is_following = profile_user.is_following(request.user)
            is_follower = request.user.is_following(profile_user)
    else:
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
    return render_to_response('public_profile.html', {'profile': profile, 
                                                            'counters': counters.get_result(),
                                                            'timeline': timeline, 
                                                            'is_following': is_following,
                                                            'is_follower': is_follower, 
                                                            'show_followers': settings.show_followers,
                                                            'show_followings': settings.show_followings
                                                            }, context_instance=RequestContext(request))


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
def profile_settings(request):
    cookie = get_user_from_cookie(request.COOKIES)
    if cookie:
        
        #Comprobamos que el toque es aún válido
        fb_client=FacebookClient(cookie["access_token"])
        if not fb_client.token_is_valid():
            #Si el usuario ya no tiene instalada la app lo lleva a instalar
            args={}
            args["permissions"]=settings.OAUTH['facebook']['scope']
            return HttpResponseRedirect('/fb/')
        
        
        access_token=OAUTH_Access.get_token(cookie["access_token"])
        if not access_token:
            # Autentica al usuario con cookie["access_token"] y si no 
            # existe tal usuario lo crea y lo devuelve           
            fb_client=FacebookClient(cookie["access_token"])
            user=fb_client.authenticate()
            access_token=OAUTH_Access.get_token(cookie["access_token"])
    
        else:
            fb_client=FacebookClient(access_token.token_key)
            fb_client.authenticate()
        
        followers=len(request.user.get_followers()[1])
        followings=len(request.user.get_followings()[1])
        #~ args['followers']=followers[1]
        
        return  render_to_response('profile.html',{'followers': followers, 'followings': followings},RequestContext(request))
    else:
        return HttpResponseRedirect('/fb/')


@facebook_required
def followers_panel(request, username):
    if username == request.user.username:
        followers=request.user.get_followers()
    else:
        user=User.objects.get_by_username(username)
        if user is None:
            raise Http404
        if user.settings.show_followers:
            followers = request.user.get_followers()
        else:
            followers = None
    return  render_to_response('followers.html', {'followers': followers}, RequestContext(request))


@facebook_required
def followings_panel(request, username):
    if username == request.user.username:
        followings=request.user.get_followings()
    else:
        user = User.objects.get_by_username(username)
        if user is None:
            raise Http404
        if user.settings.show_followings:
            followings = request.user.get_followings()
        else:
            followings = None
    return  render_to_response('followings.html', {'followings': followings}, RequestContext(request))
    
