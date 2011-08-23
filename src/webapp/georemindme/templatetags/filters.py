# coding=utf-8

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def private(value, arg):
    private = getattr(value,arg)
    if callable(private):
        return private
    return private