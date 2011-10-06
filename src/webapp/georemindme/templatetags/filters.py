# coding=utf-8

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def private(value, arg):
    private = getattr(value,arg)
    if callable(private):
        return private()
    return private


@register.filter(name='twitterize')
def twitterize(token):
    import re
    token =  re.sub(r'(@(\w+))', r'<a href="https://twitter.com/\2">\1</a>', token)
    token =  re.sub(r'(#(\w+))', r'<a href="http://twitter.com/#!/search/\2">\1</a>', token)
    
    return token
twitterize.is_safe = True

