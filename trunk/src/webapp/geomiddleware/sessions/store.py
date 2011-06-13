#coding=utf-8

import time

from models import _Session_Data, _Session_Dict


class SessionStore(object):
    
    _accessed = False
    _modified = False
    _anonymous = False
    _remember = False
    
    @property
    def session_id(self):
        return self._session.id
    
    def __iter__(self):
        return self._session._decoded
    
    def __getitem__(self, key):
        self._accessed = True
        return self._session[key]
    
    def __setitem__(self, key, value):
        self._session[key] = value
        self._modified = True
        
    def __contains__(self, key):
        return self._session.__contains__(key)
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        return True
    
    def get(self, keyname, default = None):
        try:
            return self.__getitem__(keyname)
        except KeyError:
            return default
        
    @property
    def data(self):
        return self._session._decoded
    
    def __init__(self, session=None, session_data=None, from_cookie=True):
        if session is None:
            if from_cookie:  # la nueva sesion es de usuario web
                self._session = _Session_Data.new_session(session_data=session_data)
            else:
                self._session = _Session_Dict.new_session(session_data=session_data)
                self._anonymous = True
        else:
            self._session = session
            self._accessed = True
    
    @classmethod
    def load(cls, session_id=None, session_data=None, from_cookie=True):
        '''
        Recupera la sesion o crea una nueva
        '''
        if from_cookie:
            if session_id is not None:   # recupera la sesion
                session = _Session_Data.restore_session(session_id)
                if session is not None:  # es valida
                    return SessionStore(session=session, from_cookie=from_cookie)
        # inicia una sesion nueva temporal
        return SessionStore(session_data=session_data, from_cookie=False)
    
    def init_session(self, remember=False):
        '''
        Login de un usuario, guarda la sesion en datastore
        '''
        self._session = _Session_Data.new_session(session_data=self.data)
        self._anonymous = False
        self._remember=remember
        
    def cookie_saved(self):
        return self._remember
    
    def get_expires(self):
        '''
            Fecha hasta que la sesion caduca
        '''
        return self._session.expires
    
    def get_expiry_age(self):
        '''
            Tiempos en segundos hasta que la sesion caduca
        '''
        return self._session.get_expiry_age()
    
    def clear(self):
        '''
            Borra todos los datos de la sesion
        '''
        self._session.clear()
        
    def put(self):
        '''
            Actualiza en el datastore
        '''
        if hasattr(self._session, 'put'):
            self._session.put()
            
    def delete(self):
        # FIXME : no borra el diccionario, lo pone como datos en la cookie
        self.clear()
        if hasattr(self._session, 'delete'):
            self._session.delete()
        self._anonymous = True
        self._session = _Session_Dict.new_session()
        
#  TODO: borrar sesiones antiguas