# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geoalert.views',
    url(r'^(?i)event/(?P<id>[^/]*)/$', 'suggestion_profile'),
	url(r'^suggestions/$', 'user_suggestions', {}, 'user_suggestions'),
    url(r'^suggestions/add/', 'add_suggestion', {}, 'add_suggestion'),
    url(r'^suggestion/(?P<slug>[^/]*)/$', 'suggestion_profile',{},'view_suggestion'),
    url(r'^suggestions/edit/(?P<suggestion_id>\d+)/$', 'edit_suggestion', {}, 'edit_suggestions'),
    url(r'^suggestions/cron/$', 'cron_suggestions', {}, 'cron_suggestions'),
    url(r'^(?i)place/gref/(?P<reference>[^/]*)/$', 'add_from_google_reference'),
    url(r'^(?i)place/(?P<slug>[^/]*)/$', 'view_place',{},'view_place'),
)
