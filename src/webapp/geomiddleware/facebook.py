# coding=utf-8

from django.conf import settings


class FacebookMiddleware(object):
    def process_request(self, request):
        from geoauth.clients.facebook import FacebookClient, get_user_from_cookie, parse_signed_request, OAUTHException
        if 'signed_request' in request.REQUEST:
            try:
                data = parse_signed_request(request.REQUEST['signed_request'])
                request.method = 'GET'
                request.csrf_processing_done = True
                from facebookApp.watchers import new_suggestion, new_list, new_comment, new_vote, deleted_post
                if 'oauth_token' in data:
                    request.facebook = {'uid': data['user_id'],
                                    'access_token': data['oauth_token'],
                                    'client': FacebookClient(data['oauth_token'])
                                    }
                return
            except:
                request.csrf_processing_done = False
        else:
            cookie = get_user_from_cookie(request.COOKIES)
            if cookie is not None:
                try:
                    request.facebook = {'uid': cookie['uid'],
                                        'access_token': cookie['access_token'],
                                        'client': FacebookClient(cookie['access_token'])
                                    }
                    request.csrf_processing_done = True
                    from facebookApp.watchers import new_suggestion, new_list, new_comment, new_vote, deleted_post
                    return
                except:
                    request.csrf_processing_done = False
        from facebookApp.watchers import disconnect_all
        disconnect_all()
                    

