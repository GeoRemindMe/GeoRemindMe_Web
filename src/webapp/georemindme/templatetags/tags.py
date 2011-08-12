# coding=utf-8

from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern+'$', request.path):
        return 'active-section'
    return ''


@register.tag
def timeline_item(parser, token):
    try:
        item = token.contents.split()[1]
    except ValueError:
        raise template.TemplateSyntaxError, "Tag requires one argument (timeline item)"
    
    return RenderTimelineNode(item)


class RenderTimelineNode(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)
        
    def render(self, context):
        item = self.item.resolve(context)
        t = template.loader.get_template('timeline/%s.html' % item['msg_id'])
        context['obj'] = item
        return t.render(context)


@register.filter 
def naturaltime(value, arg=None): 
    """ 
    https://code.djangoproject.com/attachment/ticket/12771/humanize%2Bnaturaltime.diff
    
    For date and time values shows how many seconds, minutes or hours ago compared to 
    current timestamp returns representing string. Otherwise, returns a string 
    formatted according to settings.DATE_FORMAT 
    """ 
    from datetime import datetime
    from django.utils.translation import ugettext as _
    try: 
        value = datetime(value.year, value.month, value.day, value.hour, value.minute, value.second) 
    except AttributeError: 
        return value 
    except ValueError: 
        return value 
    delta = datetime.now() - value 
    if delta.days > 0: 
        value = datetime(value.year, value.month, value.day, value.hour, value.minute) 
        return value #.strftime("%d/%m/%y %H:%M")
    elif delta.seconds == 0: 
        return _(u'ahora mismo') 
    elif delta.seconds < 60: 
        return _(u"hace %s segundos" % (delta.seconds)) 
    elif delta.seconds / 60 < 2: 
        return _(r'hace un minuto') 
    elif delta.seconds / 60 < 60: 
        return _(u"hace %s minutos" % (delta.seconds/60)) 
    elif delta.seconds / 60 / 60 < 2: 
        return _(u'hace una hora') 
    elif delta.seconds / 60 / 60 < 24: 
        return _(u"hace %s horas" % (delta.seconds/60/60)) 
    value = datetime(value.year, value.month, value.day) 
    return value

"""
    django templates tags for images
    @author: R. BECK
    @version: 0.1
"""

#from __future__ import with_statement #Python 2.5

import base64
import os

class EmbeddedImgNode(template.Node):
    """Image node parser for rendering html inline base64 image"""
    
    def __init__(self, item):
        self.item = template.Variable(item)

    def _encode_img(self, file_path):
        """Returns image base64 string representation and makes a cache file"""
        import memcache
        filename   = file_path.rpartition(os.sep)[2]
        cache_file = "%s_cache" % file_path
        cached_image = memcache.get('%s%s' % (memcache.version, cache_file))
        if cached_image is None:
            image = open(file_path)
            cached_image = "data:image;base64,%s"%base64.b64encode(image)
            memcache.set('%s%s' % (memcache.version, cache_file), cached_image, 300)
        return cached_image


    def _render_img(self):
        """Prepare image attributes"""
        return self._encode_img(self.item)


    def render(self, context):
        image = self._render_img()
        return image



@register.tag(name="embedded_img")
def do_embedded_img(parser, token):
    try:
        item = token.contents.split()[1]
    except ValueError:
        raise template.TemplateSyntaxError, "embedded_img requires one argument"    
    return EmbeddedImgNode(item)


@register.tag(name="embedded_avatar")
def do_embedded_avatar(parser, token):
    try:
        item = token.contents.split()[1]
    except ValueError:
        raise template.TemplateSyntaxError, "embedded_avatar requires one argument: username"
    return EmbeddedAvatarNode(item)


class EmbeddedAvatarNode(template.Node):
    """Image node parser for rendering html inline base64 image"""
    
    def __init__(self, item):
        self.item = template.Variable(item)

    def _encode_img(self):
        """Returns image base64 string representation and makes a cache file"""
        import memcache
        encoded_image = memcache.get('%s%s_avatarcache' % (memcache.version, self.item))
        if encoded_image is None:
            from geouser.views import get_avatar
            try:
                image_url = get_avatar(self, self.item)
                from libs.httplib2 import Http, HTTPSConnectionWithTimeout
                from mapsServices.places.GPRequest import Client
                mem = Client()
                req = Http(cache=mem)
                response, content = req.request(image_url['Location'])
                cached_image = "data:image;base64,%s" % base64.b64encode(content)
                memcache.set('%s%s_avatarcache' % (memcache.version, self.item), encoded_image, 300)
            except:
                return 'http://georemindme.appspot.com/static/facebookApp/img/no_avatar.png'
        return cached_image

    def render(self, context):
        self.item = self.item.resolve(context)
        image = self._encode_img()
        context['image_b64'] = self.item
        return image