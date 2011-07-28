# coding=utf-8

"""
.. module:: mails
    :platform: appengine
    :synopsis: Correos enviados desde geouser
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

        url = 'http://%s/confirm/%s/%s' % (host, base64.urlsafe_b64encode(to.encode("utf-8")), confirm_code)
        return url

    """
        Send registration mail confirmation
    """
    if to is None or confirm_code is None:
        raise ValueError()    
    
    translation.activate(language)
    message = GeoMail()    
    message.to = to
    message.subject = _("Confirm your registration at GeoRemindMe")
    message.body = _("""
        Confirm your registration at GeoRemindMe, copy and paste this url:
        %(url)s
        """) % {
                    'url': generate_confirm_url(to, confirm_code)
                }
    message.html = _("""
        <html><head></head><body>
        Confirm your registration at GeoRemindMe
        %(link)s
        If you don't see the link, copy and paste this url:
        %(url)s
        </body></html>
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

        url = 'http://%s/remind/%s/%s' % (host, base64.urlsafe_b64encode(to.encode("utf-8")), remind_code)
        return url

    """
        Send registration mail confirmation
    """
    if to is None or remind_code is None:
        raise ValueError()
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("Set a new password at GeoRemindMe")
    message.body = _("""
        Set a new password at GeoRemindMe, copy and paste this url:
        %(url)s
        """) % {
                    'url': generate_remind_pass_url(to, remind_code)
                }
    message.html = _("""
        <html><head></head><body>
        Set a new password at GeoRemindMe
        %(link)s
        If you don't see the link, copy and paste this url:
        %(url)s
        </body></html>
        """) % {
                    'link': generate_remind_pass_link(to, remind_code),
                    'url': generate_remind_pass_url(to, remind_code)
                }
    translation.deactivate()
    message.push()
    
def send_notification_follower(to, follower, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s is now following you at Georemindme") % follower
    message.body = _("""
        %(username)s new follower
        """) % {
                    'username': follower.username,
                }
    message.html = _("""
        <html><head></head><body>
        %(username)s new follower
        </body></html>
        """) % {
                    'username': follower.username,
                }
    translation.deactivate()
    message.push()
    
    
def send_notification_suggestion_follower(to, suggestion, user, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s is now following your suggestion: %s at Georemindme") % (user, suggestion.name)
    message.body = _("""
        %(suggestion)s new follower %s(username)s
        """) % {
                    'suggestion': suggestion.name,
                    'username': user.username,
                }
    message.html = _("""
        <html><head></head><body>
        %(suggestion)s new follower %s(username)s
        </body></html>
        """) % {
                    'suggestion': suggestion.name,
                    'username': user.username,
                }
    translation.deactivate()
    message.push()
    
def send_notification_suggestion_comment(to, comment, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s commented in your suggestion: %s at Georemindme") % (comment.user, comment.instance.name)
    message.body = _("""
        %(suggestion)s new comment %s(username)s
        %(msg)s
        """) % {
                    'suggestion': comment.instance.name,
                    'username': comment.user.username,
                    'msg': comment.msg,
                }
    message.html = _("""
        <html><head></head><body>
        %(suggestion)s new comment %s(username)s
        <br>%(msg)s
        </body></html>
        """) % {
                    'suggestion': comment.instance.name,
                    'username': comment.user.username,
                    'msg': comment.msg,
                }
    translation.deactivate()
    message.push()
    
def send_notification_account_summary(to, user, followers, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("Report of your account %s at Georemindme") % user
    names = ', '.join(str(follow) for follow in followers)
    message.body = _("""
        New followers:
        %(names)s
        """) % {
                    'names': names
                }
    message.html = _("""
        <html><head></head><body>
        New followers:
        <br/ >%(names)s
        </body></html>
        """) % {
                    'names': names
                }
    translation.deactivate()
    message.push()
    
def send_notification_suggestion_summary(to, suggestions, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("Summary of your suggestions at Georemindme")
    message.body = _("""
        %(suggestion)s
        """) % {
                    'suggestion': suggestions,
                }
    message.html = _("""
        <html><head></head><body>
        %(suggestion)s
        </body></html>
        """) % {
                    'suggestion': suggestions,
                }
    translation.deactivate()
    message.push()
    
