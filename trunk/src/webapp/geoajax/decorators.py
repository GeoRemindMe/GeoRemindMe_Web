# coding=utf-8

from django.http import HttpResponseBadRequest


def ajax_request(func):
    def _wrapper(*args, **kwargs):
        request = args[0]
        if request.method <> "POST" or not request.is_ajax():
            return HttpResponseBadRequest("Not AJAX or POST", mimetype="text/plain")
        return func(*args, **kwargs)
    return _wrapper