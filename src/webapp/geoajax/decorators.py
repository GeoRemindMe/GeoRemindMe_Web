# coding=utf-8

from django.http import HttpResponseBadRequest,HttpResponse


def ajax_request(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        if request.method not in ("POST","OPTIONS",) or not request.is_ajax():
            return HttpResponseBadRequest("Not AJAX or POST", mimetype="text/plain")
        return func(*args, **kwargs)
    return _wrapper

"""
    This allow a view be called from HTTP
"""
def allow_crossdomain(func,domains="http://georemindme.appspot.com"):
    def _wrapper(*args, **kwargs):
        
        request = args[0]
        
        if request.method == "OPTIONS":
            resp = HttpResponse()
        else:
            resp = func(*args, **kwargs)
        
        if resp.status_code == 200:
            resp['Access-Control-Allow-Origin'] = domains.join(',') if hasattr(domains, '__iter__') else domains
            #resp['Access-Control-Allow-Credentials'] = "true"
            resp['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS"
            #resp['Access-Control-Max-Age'] = "1728000"
            
        return resp
    return _wrapper
