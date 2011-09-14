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
    message.subject = _("Correo de confirmación de GeoRemindMe")
    message.body = _("""
        Muchas gracias por darte de alta en GeoRemindMe!, para terminar de activar tu cuenta solo tiene que
        haz clic en el siguiente enlace para que podamos verificar que esta cuenta de correo es tuya:\n
        %(url)s\n
        \n
        Si has recibido este correo por error por favor escríbenos a info@georemindme.com para que podamos comprobar
        que ha pasado.\n
        \n
        Muchas gracias,\n
        El equipo de GeoRemindMe!
        """) % {
                    'url': generate_confirm_url(to, confirm_code)
                }
    message.html = _("""
        <html><head></head><body>
        <p>
        Muchas gracias por darte de alta en GeoRemindMe!, para terminar de activar tu cuenta solo tiene que
        haz clic en el siguiente enlace para que podamos verificar que esta cuenta de correo es tuya:<br>
        %(link)s
        </p>
        <p>
        Si no ves este enlace por favor abre tu navegador y escribe la siguiente dirección:<br>
        %(url)s
        </p>
        <p>
        Si has recibido este correo por error por favor escríbenos a info@georemindme.com para que podamos comprobar
        que ha pasado.
        </p>
        <p>
        Muchas gracias,
        El equipo de GeoRemindMe!
        </p>
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
    message.subject = _("Solicitud de nueva contraseña en GeoRemindMe!")
    message.body = _("""
        Hemos recibido una petición de cambio de contraseña, para hacer el cambio tan solo \n
        tienes que acceder a esta página:\n
        %(url)s\n
        \n
        Si has recibido este correo por error por favor escríbenos a info@georemindme.com para que podamos comprobar
        que ha pasado.\n
        \n
        Muchas gracias,\n
        El equipo de GeoRemindMe!
        """) % {
                    'url': generate_remind_pass_url(to, remind_code)
                }
    message.html = _("""
        <html><head></head><body>
        <p>
        Hemos recibido una petición de cambio de contraseña, para hacer el cambio tan 
        solo tienes que acceder a esta página:<br>
        %(link)s
        </p>
        <p>
        Si no ves este enlace por favor abre tu navegador y escribe la siguiente dirección:<br>
        %(url)s
        </p>
        <p>
        Si has recibido este correo por error por favor escríbenos a info@georemindme.com para que podamos comprobar
        que ha pasado.<br>
        Muchas gracias,
        El equipo de GeoRemindMe!
        </p>
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
    message.subject = _("%s te está siguiendo ahora en Georemindme!") % follower
    message.body = _("""
        %(username)s te está siguiendo ahora, puedes ver su perfil en:\n
        %(user_profile)s\n
        \n
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a traves de
        tu perfil en www.georemindme.com\n
        \n
        Muchas gracias,\n
        El equipo de GeoRemindMe!
        """) % {
                    'username': follower.username,
                    'user_profile': follower.get_absolute_url
                }
    message.html = _("""
        <html><head></head><body>
        %(username)s te está siguiendo ahora, puedes ver su perfil en:<br>
        <a href="%(user_profile)s">%(user_profile)s</a><br>
        <br>
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a traves de
        tu perfil en <a href="http://www.georemindme.com">www.georemindme.com</a>\n
        <br>
        Muchas gracias,<br>
        El equipo de GeoRemindMe!
        </body></html>
        """) % {
                    'username': follower.username,
                    'user_profile': follower.get_absolute_url
                }
    translation.deactivate()
    message.push()
    
    
def send_notification_suggestion_follower(to, suggestion, user, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s ha guardado tu sugerencia: \"%s\" en GeoRemindMe!") % (user, suggestion.name)
    message.body = _("""
        El usuario %s(username)s ha guardado tu sugerencia '%(suggestion)s' en su mochila para no olvidarse de hacerla
        y poder compartirla con otros usuarios.\n
        \n
        Si quieres ver las sugerencias de %s(username)s puedes acceder a su perfil en esta dirección:\n
        %s(user_profile)s\n
        \n
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a traves de
        tu perfil en www.georemindme.com\n
        \n
        Muchas gracias,\n
        El equipo de GeoRemindMe!
        
        """) % {
                    'suggestion': suggestion.name,
                    'username': user.username,
                    'user_profile':user.get_absolute_url
                }
    message.html = _("""
        <html><head></head><body>
        <p>
        El usuario %s(username)s ha guardado tu sugerencia '%(suggestion)s' en su mochila para no olvidarse de hacerla
        y poder compartirla con otros usuarios.
        </p>
        <p>
        Si quieres ver las sugerencias de %s(username)s puedes acceder a su perfil en esta dirección:\n
        <a href="%s(user_profile)s">%s(user_profile)s</a>
        </p>
        <p>
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en <a href="http://www.georemindme.com">www.georemindme.com</a>
        </p>
        <p>
        Muchas gracias,<br>
        El equipo de GeoRemindMe!
        </p>
        </body></html>
        """) % {
                    'suggestion': suggestion.name,
                    'username': user.username,
                    'user_profile':user.get_absolute_url
                }
    translation.deactivate()
    message.push()
    
def send_notification_suggestion_comment(to, comment, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("%s commented in your suggestion: %s at Georemindme") % (comment.user, comment.instance.name)
    message.body = _("""
        El usuario %s(username)s ha hecho el siguiente comentario en tu sugerencia '%(suggestion)s':
        %(msg)s\n
        \n
        Si quieres responderle tan solo tienes que acceder acceder a la siguiente dirección:\n
        %s(suggestion_link)s\n
        \n
        Y una vez identificado podrás responder.
        \n
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com\n
        \n
        Muchas gracias,\n
        El equipo de GeoRemindMe!
        %(suggestion)s new comment %s(username)s
        
        """) % {
                    'suggestion': comment.instance.name,
                    'username': comment.user.username,
                    'msg': comment.msg,
                    'suggestion_link': comment.instance.short_url,
                }
    message.html = _("""
        <html><head></head><body>
        <p>
        El usuario %s(username)s ha hecho el siguiente comentario en tu sugerencia '%(suggestion)s':
        %(msg)s<br>
        </p>
        <p>
        Si quieres responderle tan solo tienes que acceder acceder a la siguiente dirección:<br>
        %s(suggestion_link)s
        </p>
        <p>
        Y una vez identificado podrás responder.
        </p>
        <p>
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com<br>
        </p>
        <p>
        Muchas gracias,<br>
        El equipo de GeoRemindMe!
        </p>
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
    message.subject = _("Personas que han empezado a seguirte esta semana en Georemindme")
    names = '\n- '.join(str(follow) for follow in followers)
    names_html = '<br>- '.join(("<a href=\"%(link)s\">%(username)s</a>") % {'username':str(follow),'link':str(follow.get_absolute_url)} for follow in followers)
    message.body = _("""
        ¡Hola %(username)s!,\n
        Esta semana han empezado a seguirte %(num_followers)d personas.\n
        Aquí puede ver un listado:
        %(names)s\n
        \n
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com\n, y sino...¡hasta la semana que viene!\n
        El equipo de GeoRemindMe!
        """) % {
                    'names': names,
                    'username':user.username,
                    'num_followers':len(followers)
                }
    message.html = _("""
        <html><head></head><body>
        ¡Hola %(username)s!,<br>
        Esta semana han empezado a seguirte %(num_followers)d personas.<br>
        Aquí puede ver un listado:
        <p>
        %(names_html)s
        </p>
        <p>
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com\n, y sino...¡hasta la semana que viene!<br>
        El equipo de GeoRemindMe!
        </p>
        </body></html>
        """) % {
                    'names': names,
                    'username':user.username,
                    'num_followers':len(followers)
                }
    translation.deactivate()
    message.push()
    
def send_notification_suggestion_summary(to, suggestions, language='en'):
    translation.activate(language)
    message = GeoMail()
    message.to = to
    message.subject = _("Resumen de la actividad en tus sugerencias - GeoRemindMe!")
    message.body = _("""
        Aquí te dejamos un resumen de los comentarios, valoraciones, etc que han recibido tus sugerencias a lo largo de la semana\n
        %(suggestion)s\n
        \n
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com\n, y sino...¡hasta la semana que viene!\n
        El equipo de GeoRemindMe!
        """) % {
                    'suggestion': suggestions,
                }
    message.html = _("""
        <html><head></head><body>
        <p>
        Aquí te dejamos un resumen de los comentarios, valoraciones, etc que han recibido tus sugerencias a lo largo de la semana<br>
        %(suggestion)s
        </p>
        <p>
        Si quieres cambiar la configuración de tus notificaciones, puedes hacerlo a través de
        tu perfil en www.georemindme.com\n, y sino...¡hasta la semana que viene!<br>
        El equipo de GeoRemindMe!
        </p>
        </body></html>
        """) % {
                    'suggestion': suggestions,
                }
    translation.deactivate()
    message.push()
    
