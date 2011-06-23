# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geoajax.views',
    (r'^(?i)delete/reminder/$', 'delete_reminder'),
    (r'^(?i)delete/following/$', 'del_following'),
    (r'^(?i)add/following/$', 'add_following'),
    (r'^(?i)add/reminder/$', 'add_reminder'),
    (r'^(?i)add/following/$', 'add_following'),
    (r'^(?i)get/reminder/$', 'get_reminder'),
    (r'^(?i)get/followers/$', 'get_followers'),
    (r'^(?i)get/followings/$', 'get_followings'),
    (r'^(?i)get/timeline/$', 'get_timeline'),
    (r'^(?i)get/chronology/$', 'get_chronology'),
	(r'^(?i)login/$', 'login'),
	(r'^(?i)register/$', 'register'),
	(r'^(?i)exists/$', 'exists'),
	(r'^(?i)contact/$', 'contact'),
	(r'^(?i)keep-up-to-date/$', 'keepuptodate'),

)
