# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""
import base64
from google.appengine.api import mail

from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils import translation

from georemindme.geomail import GeoMail


def send_confirm_mail(to=None, confirm_code=None, language='en'):
    def generate_confirm_link(to, confirm_code):
        url = _('<a href="%s">Confirmation link</a>') % generate_confirm_url(to, confirm_code)
        return url

    def generate_confirm_url(to, confirm_code):
        import os
        host = os.environ['HTTP_HOST']

        url = 'http://%s/confirm/%s/%s' % (host, base64.encodestring(to), confirm_code)
        return url

    """
        Send registration mail confirmation
    """
    if to is None or confirm_code is None:
        raise ValueError()    
    
    translation.activate(language)
    message = GeoMail()    
    message.sender = 'noreply@georemind.me'
    message.to = to
    message.subject = _("Confirm your registration at GeoRemindMe")
    message.html = _("""Confirm your registration at GeoRemindMe
                    %(link)s
                    If you don't see the link, copy and paste this url:
                    %(url)s
                    """) % {
                            'link': generate_confirm_link(to, confirm_code),
                            'url': generate_confirm_url(to, confirm_code)
                            }
    translation.deactivate()
    message.push()


def send_remind_pass_mail(to=None, remind_code=None, language='en'):
    def generate_remind_pass_link(to, remind_code):
        url = _('<a href="%s">Password reminder link</a>') % generate_remind_pass_url(to, remind_code)
        return url

    def generate_remind_pass_url(to, confirm_code):
        import os
        host = os.environ['HTTP_HOST']

        url = 'http://%s/remind/%s/%s' % (host, base64.encodestring(to), remind_code)
        return url

    """
        Send registration mail confirmation
    """
    if to is None or remind_code is None:
        raise ValueError()
    translation.activate(language)
    message = GeoMail()
    message.sender = 'noreply@georemind.me'
    message.to = to
    message.subject = _("Set a new password at GeoRemindMe")
    message.html = _("""Set a new password at GeoRemindMe
                    %(link)s
                    If you don't see the link, copy and paste this url:
                    %(url)s
                    """) % {
                            'link': generate_remind_pass_link(to, remind_code),
                            'url': generate_remind_pass_url(to, remind_code)
                            }
    translation.deactivate()
    message.push()
    
def send_notification_follower(to, follower, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.sender = 'noreply@georemind.me'
    message.to = to
    message.subject = _("%s is now following you at Georemindme") % follower
    message.html = _("""
                        follower
                    """)
    translation.deactivate()
    message.push()
    
