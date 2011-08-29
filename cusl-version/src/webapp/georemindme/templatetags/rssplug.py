# coding=utf-8
# rssplug.py
# Alberto García Hierro
# Drop this file inside your templatetags folder
# See http://fi.am/entry/plugging-a-rss-feed-into-a-django-template/

from datetime import datetime
import time

#from django.core.cache import cache
from django import template

import feedparser

register = template.Library()

@register.filter
def todatetime(value):
    return datetime(*time.localtime(time.mktime(value))[:6])

@register.tag
def rssplug(parser, token):
    try:
        tag_name, address, template, num = token.split_contents()
        num = int(num)
    except ValueError:
        raise template.TemplateSyntaxError('%s tag requires 3 arguments' % token.split_contents()[0])

    return RssPlugNode(address, template, num)

def resolve(var_or_value, ctx):
    if var_or_value[0] == '"':
        return var_or_value[1:-1]

    return ctx.resolve_variable(var_or_value)

class RssPlugNode(template.Node):
    def __init__(self, address, templ, num):
        self.address = address
        self.templ = templ
        self.num = num

    # NO CACHED!
    def rss(self, addr):
        #ckey = 'rssplug_%s' % addr
        #data = cache.get(ckey)
        #if data:
        #    return data
        data = feedparser.parse(addr)
        #cache.set(ckey, data)
        return data

    def render(self, context):
        address = resolve(self.address, context)
        tmpl = resolve(self.templ, context)
        t = template.loader.get_template(tmpl)
        entries = self.rss(address).entries[:self.num]
        return ''.join([t.render(template.Context({ 'item': item })) for item in entries])
