# coding=utf-8

"""
.. module:: geomail
    :platform: appengine
    :synopsis: Clase para el envio de correos
"""


from google.appengine.api import mail
from django.utils.translation import ugettext as _
from django.conf import settings


class GeoMail(mail.EmailMessage):
    def __init__(self, *args, **kwargs):
        self.sender = 'noreply@georemind.me'
        super(self.__class__, self).__init__(*args,**kwargs)
        
    def push(self):
        """
            Añade el correo  a la cola
        """
        from tasks import EmailHandler
        EmailHandler().add(self)


def send_contact_email(org,msg,to=settings.CONTACT_EMAIL, language='en'):
    import datetime
    from django.utils import translation
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = "[GeoRemindMe] Email de contacto"
    message.body = _("""
            %(date)s
            \n %(username)s dejó el mensaje:\n"%(message)s" 
        """) % {
                 'date': str(datetime.datetime.now()),
                 'username': org,
                 'message': msg
                 }
    message.html = _("""
            <html><head></head><body>
            %(date)s<br/>%(username)s dejó el mensaje:<br/>"%(message)s" 
            </body></html>
        """) % {
                 'date': str(datetime.datetime.now()),
                 'username': org,
                 'message': msg
                 }
    translation.deactivate()
    message.push()


def send_keepuptodate(org,msg,to=settings.CONTACT_EMAIL, language='en'):
    import datetime
    from django.utils import translation
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = "[GeoRemindMe] Keep up to date"
    message.body = _("""
            %(date)s
            \n %(username)s
            \n %(message)s
        """)  % {
                 'date': str(datetime.datetime.now()),
                 'username': org,
                 'message': msg
                 }
    message.html = _("""
            <html><head></head><body>
            %(date)s<br/>%(username)s<br/>%(message)s"
            </body></html>
         """) % {
                 'date': str(datetime.datetime.now()),
                 'username': org,
                 'message': msg
                 }
    translation.deactivate()
    message.push()


def send_notification_invitation(to, sender, invitation, language='en'):
    from django.utils import translation
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s sent you a new invitation") % sender
    message.body = _("""
            blababababab
            """)
    message.html = _("""
                        <html><head></head><body>
                        blababababa
                        </body></html>
                    """)
    translation.deactivate()
    message.push()
    
