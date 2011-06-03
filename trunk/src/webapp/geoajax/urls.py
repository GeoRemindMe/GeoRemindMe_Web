# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geoajax.views',
    (r'^delete/reminder/$', 'delete_reminder'),
    (r'^delete/following/$', 'del_following'),
    (r'^add/following/$', 'add_following'),
    (r'^add/reminder/$', 'add_reminder'),
    (r'^add/following/$', 'add_following'),
    (r'^get/reminder/$', 'get_reminder'),
    (r'^get/followers/$', 'get_followers'),
    (r'^get/followings/$', 'get_followings'),
    (r'^get/timeline/$', 'get_timeline'),
    (r'^get/chronology/$', 'get_chronology'),
	(r'^login/$', 'login'),
	(r'^register/$', 'register'),
	(r'^exists/$', 'exists'),
	(r'^contact/$', 'contact'),
	(r'^keep-up-to-date/$', 'keepuptodate'),

)
