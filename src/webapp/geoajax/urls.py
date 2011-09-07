# coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('geoajax.views',
    (r'^delete/reminder/$', 'delete_reminder'),
    (r'^delete/following/$', 'delete_following'),
    (r'^delete/suggestion/$', 'delete_suggestion'),
    (r'^delete/suggestion/follower/$', 'delete_suggestion_follower'),
    (r'^delete/suggestion/list/$', 'delete_list',{}, 'delete_list'),
    (r'^delete/comment/$', 'delete_comment'),
    (r'^delete/list/follower/$', 'delete_list_follower'),
    (r'^add/following/$', 'add_following'),
    (r'^add/reminder/$', 'add_reminder'),
    (r'^add/following/$', 'add_following'),
    (r'^add/suggestion/$', 'add_suggestion'),
    (r'^add/suggestion/invitation/$', 'add_suggestion_invitation'),
    (r'^add/suggestion/follower/$', 'add_suggestion_follower'),
    (r'^add/suggestion/tags/$', 'add_suggestion_tags'),
    (r'^add/list/follower/$', 'add_list_follower'),
    (r'^suggestion/list/invitation/$', 'add_suggestion_list_invitation', {}, 'invitation_suggestion_list'),
    (r'^suggestion/list/modify/$', 'add_list_suggestion',{},'modify_suggestion_list'),
    (r'^suggestion/list/suggested/$', 'suggested_list_suggestion',{},'suggested_suggestion_list'),
    (r'^add/comment/event/$', 'do_comment', {'kind': 'Event'}),
    (r'^add/comment/list/$', 'do_comment', {'kind': 'List'}),
    (r'^get/reminder/$', 'get_reminder'),
    (r'^get/followers/$', 'get_followers'),
    (r'^get/followings/$', 'get_followings'),
    (r'^get/timeline/$', 'get_profile_timeline'),
    (r'^get/activity/$', 'get_activity_timeline',{},'get_activity_timeline'),
    (r'^get/notifications/$', 'get_notifications_timeline'),
    (r'^get/suggestion/$', 'get_suggestion'),
    (r'^get/suggestion/following/$', 'get_suggestion_following'),
    (r'^get/suggestion/list/$', 'get_list_suggestion'),
    (r'^get/suggestions/$', 'get_suggestions',{},'get_suggestions'),
    (r'^get/comment/event/$', 'get_comments', {'kind': 'Event'}),
    (r'^get/comment/list/$', 'get_comments', {'kind': 'List'}),
    (r'^get/near/places/$', 'get_near_places'),
    (r'^get/near/suggestions/$', 'get_near_suggestions'),
    (r'^search/tag/suggestions/$', 'search_tag_suggestion'),
    (r'^vote/suggestion/$', 'do_vote', {'kind': 'Event'}),
    (r'^vote/comment/$', 'do_vote', {'kind': 'Comment'}),
    (r'^vote/list/$', 'do_vote', {'kind': 'List'}),
    (r'^contacts/block/$', 'block_contacts'),
	(r'^login/$', 'login'),
	(r'^register/$', 'register'),
	(r'^exists/$', 'exists'),
	(r'^contact/$', 'contact'),
	(r'^keep-up-to-date/$', 'keepuptodate'),
    (r'^searchconfgoogle/$', 'mod_searchconfig_google'),
    (r'^get/short/$', 'get_short_url', {}, 'short_url'),
    (r'^share/facebook/$', 'share_on_facebook', {}, 'share_on_facebook'),
    (r'^share/twitter/$', 'share_on_twitter', {}, 'share_on_twitter'),
)
