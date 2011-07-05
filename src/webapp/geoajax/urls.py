# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geoajax.views',
    (r'^(?i)delete/reminder/$', 'delete_reminder'),
    (r'^(?i)delete/following/$', 'delete_following'),
    (r'^(?i)delete/suggestion/$', 'delete_suggestion'),
    (r'^(?i)add/following/$', 'add_following'),
    (r'^(?i)add/reminder/$', 'add_reminder'),
    (r'^(?i)add/following/$', 'add_following'),
    (r'^(?i)add/suggestion/$', 'add_suggestion'),
    (r'^(?i)get/reminder/$', 'get_reminder'),
    (r'^(?i)get/followers/$', 'get_followers'),
    (r'^(?i)get/followings/$', 'get_followings'),
    (r'^(?i)get/timeline/$', 'get_timeline'),
    (r'^(?i)get/chronology/$', 'get_chronology'),
    (r'^(?i)get/suggestion/$', 'get_suggestion'),
    (r'^(?i)contacts/google/$', 'get_contacts_google'),
    (r'^(?i)contacts/facebook/$', 'get_friends_facebook'),
    (r'^(?i)contacts/twitter/$', 'get_friends_twitter'),
	(r'^(?i)login/$', 'login'),
	(r'^(?i)register/$', 'register'),
	(r'^(?i)exists/$', 'exists'),
	(r'^(?i)contact/$', 'contact'),
	(r'^(?i)keep-up-to-date/$', 'keepuptodate'),

)
