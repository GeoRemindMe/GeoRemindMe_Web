from django.conf.urls.defaults import *

urlpatterns = patterns('geoauth.views',
    (r'^(?i)request_token/$', 'token_request'),
    (r'^(?i)authorize/$', 'authorize_token_request'),
    (r'^(?i)access_token/$', 'access_token_request'),
    (r'^(?i)client_request_token/(?P<provider>[^/]*)/$', 'client_token_request'),
    (r'^(?i)authenticated/facebook/$', 'facebook_authenticate_request'),
    (r'^(?i)authorized/facebook/$', 'facebook_access_request'),
    (r'^(?i)authorized/(?P<provider>[^/]*)/$', 'client_access_request'),
    (r'^(?i)authenticate/(?P<provider>[^/]*)/$', 'authenticate_request'),
    (r'^(?i)revocate/(?P<provider>[^/]*)/$', 'revocate_perms'),
)