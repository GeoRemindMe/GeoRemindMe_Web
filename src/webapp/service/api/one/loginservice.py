# coding=utf-8

from protorpc import message_types
from protorpc import messages
from protorpc.remote import ApplicationError
from protorpc import remote
from django.core.exceptions import ValidationError

from messages import LoginResponse
from mainservice import MainService


class LoginRequest(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)
    

class LoginService(MainService):
    """
        Define el servicio para obtener timelines de usuarios
    """
    #decorador para indicar los metodos del servicio
    @remote.method(LoginRequest, LoginResponse)
    def login(self, request):
        email = unicode(request.email)
        password = unicode(request.password)
        from geouser.models import User
        from django.core.validators import validate_email
        try:
            validate_email(email.decode('utf8'))
            user = User.objects.get_by_email(email)
        except ValidationError:
            user = User.objects.get_by_username(email)
        except:
            raise ApplicationError("Invalid email/password")
        if user is not None:
            if user.check_password(password):
                from geomiddleware.sessions.store import SessionStore
                session = SessionStore()
                session.init_session(remember=True, 
                                     lang=user.settings.language, 
                                     user=user, 
                                     from_rpc=True, 
                                     is_from_facebook=False)
                session.put()
                return LoginResponse(session=session.session_id, expires = session.get_expiry_age())
            else:
                raise ApplicationError("Invalid email/password")
        else:
            raise ApplicationError("Invalid email/password")    
            
        raise ApplicationError("Unknow error")

        