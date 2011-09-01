# coding=utf-8

from django.conf import settings


class FacebookMiddleware(object):
    def process_request(self, request):
        from geoauth.clients.facebook import FacebookClient, get_user_from_cookie, parse_signed_request
        if 'signed_request' in request.REQUEST:
            try:
                data = parse_signed_request(request.REQUEST['signed_request'])
                if 'oauth_token' in data:
                    request.facebook = {'uid': data['user_id'],
                                    'access_token': data['oauth_token'],
                                    'client': FacebookClient.load_client(data['oauth_token'])
                                    }
                request.csrf_processing_done = True
                request.method = 'GET'
                from facebookApp.watchers import new_suggestion, new_list, new_comment, new_vote, deleted_post
            except:
                raise
                request.csrf_processing_done = False
        else:
            cookie = get_user_from_cookie(request.COOKIES)
            if cookie is not None:
                request.facebook = cookie
                request.facebook['client'] = FacebookClient.load_client(cookie["access_token"])
                
                request.csrf_processing_done = True
                from facebookApp.watchers import new_suggestion, new_list, new_comment, new_vote, deleted_post

