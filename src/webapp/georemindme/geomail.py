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
            %s
            \n %s dejó el mensaje:\n"%s" 
        """) % (str(datetime.datetime.now()),org,msg)
    message.html = _("""
            <html><head></head><body>
            %s<br/>%s dejó el mensaje:<br/>"%s" 
            </body></html>
        """) % (str(datetime.datetime.now()),org,msg)
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
            %s
            \n %s
            \n %s
        """)  % (str(datetime.datetime.now()),org,msg)
    message.html = _("""
            <html><head></head><body>
            %s<br/>%s<br/>%s"
            </body></html>
         """) % (str(datetime.datetime.now()),org,msg)
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
    
