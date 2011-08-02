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
        from django.template import Context
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
