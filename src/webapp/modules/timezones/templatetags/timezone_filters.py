from datetime import datetime

from django.template import Library
from django.conf import settings
from django.utils.tzinfo import LocalTimezone
from django.utils.timesince import timesince
from django.utils.translation import ugettext_lazy as _

from timezones.utils import localtime_for_timezone

register = Library()

FORMAT_TIMESINCE = {
                 'uploaded' : {'date' : _("%s"), 'ago' : _("%s ago") }, 
                 'written'  : {'date' : _("%s"), 'ago' : _("%s ago") }, 
                 }

def localtime(value, user):
    if not user.is_authenticated():
        timezone = settings.TIME_ZONE
    else:
        timezone = user.get_profile().timezone
    return localtime_for_timezone(value, timezone)
register.filter("localtime", localtime)


@register.filter
def date_timesince(d, format='uploaded'):
    f_time = FORMAT_TIMESINCE[format]
    
    if getattr(d, 'tzinfo', None):
        now = datetime.now(LocalTimezone(d))
    else:
        now = datetime.now()
    
    if ( now - d ).days < 1:
        return _(f_time['ago'] % timesince(d, now) )
    
    else:
        return _(f_time['date'] % d.strftime("%d/%m/%y") ) 
