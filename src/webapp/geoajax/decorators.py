# coding=utf-8

from django.http import HttpResponseBadRequest


def ajax_request(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        if request.method != "POST" or not request.is_ajax():
            return HttpResponseBadRequest("Not AJAX or POST", mimetype="text/plain")
        return func(*args, **kwargs)
    return _wrapper

"""
    This allow a view be called from HTTP
"""
def allow_crossdomain(func,domains="http://georemindme.appspot.com"):
    def _wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        
        if resp.status_code == 200:
            resp['Access-Control-Allow-Origin'] = domains
            
        return resp
    return _wrapper
