# coding=utf-8

from django import template
from django.template.defaultfilters import stringfilter

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
        try:
            item = self.item.resolve(context)
            t = template.loader.get_template('timeline/%s.html' % item['msg_id'])
            context['obj'] = item
            return t.render(context)
        except Exception, e:
            import logging
            logging.error('ERROR EN TIMELINE %s: %s' % (item['msg_id'], e.message))


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


@register.simple_tag
def embedded_avatar(username):
    import memcache
    encoded_image = memcache.get('%s%s_avatarcachebase64' % (memcache.version, username))
    if encoded_image is None:
        from geouser.views import get_avatar
        try:
            image_url = get_avatar(None, username)
            from google.appengine.api import urlfetch
            result = urlfetch.fetch(image_url['Location'])
            encoded_image = "data:image;base64,%s" % base64.b64encode(result.content)
            memcache.set('%s%s_avatarcachebase64' % (memcache.version, username), encoded_image, 1123)
        except:
            return 'https://georemindme.appspot.com/static/facebookApp/img/no_avatar.png'
    return encoded_image


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


@register.tag(name='assign')
def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


@register.tag
def url2(parser, token):
    """
    based on default tag
    """
    bits = token.split_contents()
    if len(bits) < 2:
        from django.template import TemplateSyntaxError
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    in_facebook = parser.compile_filter(bits[1])
    viewname = bits[2]
    args = []
    kwargs = {}
    asvar = None
    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    import re
    kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return URL2Node(viewname, args, kwargs, asvar, legacy_view_name=True, in_facebook=in_facebook)

class URL2Node(template.Node):
    def __init__(self, view_name, args, kwargs, asvar, legacy_view_name=True, in_facebook=False):
        self.view_name = view_name
        self.in_facebook = in_facebook
        self.legacy_view_name = legacy_view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        from django.conf import settings
        args = [arg.resolve(context) for arg in self.args]
        from django.utils.encoding import smart_str
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        view_name = self.view_name
        in_facebook = self.in_facebook.resolve(context)
        if not self.legacy_view_name:
            view_name = view_name.resolve(context)
        if in_facebook and view_name.find('fb_') == -1:
            view_name = '%s%s' % ('fb_', view_name)
        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + '.' + view_name,
                              args=args, kwargs=kwargs,
                              current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url
        
        