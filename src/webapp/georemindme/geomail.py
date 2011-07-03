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

from google.appengine.api import mail

from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils import translation

from tasks import EmailHandler


class GeoMail(mail.EmailMessage):
    def __init__(self, *args, **kwargs):
        self.sender = 'noreply@georemind.me'
        super(self.__class__, self).__init__(*args,**kwargs)
        
    def push(self):
        '''
        Añade el correo  a la cola
        '''
        EmailHandler().add(self)

def send_contact_email(org,msg,to=settings.CONTACT_EMAIL,):

    import datetime
    
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
    message.push()
    
def send_keepuptodate(org,msg,to=settings.CONTACT_EMAIL,):

    import datetime
    
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
    message.push()
    
def send_notification_invitation(to, sender, invitation, language='en'):
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
    
