import base64
import pickle
import datetime
import time
from google.appengine.ext import db

class _Session_Data(db.Model):
    session_data = db.TextProperty()
    expires = db.DateTimeProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    from_cookie = False
    
    _decoded = {}
    
    @property
    def key(self):
        if self.is_saved():
            return self.key()
        return None
    
    def decode(self):
        if len(self._decoded) != 0:
            return self._decoded
        encoded = base64.decodestring(self.session_data)
        try:
            self._decoded = pickle.loads(encoded)
            return self._decoded
        except:  # no se pueden cargar los datos, estan corruptos??
            self._decoded = {}
            return {}
        
    def encode(self, dict):
        self._decoded = dict
        pickled = pickle.dumps(dict)
        self.session_data = base64.encodestring(pickled)
        
    def clear(self):
        self._decoded = {}
        
    def put(self, **kwargs):
        if not self.from_cookie:
            super(_Session_Data, self).put(**kwargs)
        
        
class SessionStore(object):
    
    _accessed = False
    _modified = False
    _anonymous = False
    
    def __init__(self, session=None, session_data=None):
        if session is None:
            self._session = _Session_Data(session_data=session_data, from_cookie=True)
            self.anonymous = True
        self._session = session
        self._accessed = True
    
    @classmethod
    def load(cls, session_key=None, session_data=None):
        if session_key is not None:  # cargar sesion de usuario identificado
            session = _Session_Data.get(session_key)
            if session is not None and session.expire_date < datetime.datetime.now():
                return SessionStore(session=session)
        return SessionStore(session_data=session_data)
    
    def get_expires(self):
        return self._session.expires
    
    def get_expiry_age(self):
        return time.mktime(self.get_expires().timetuple())
    
    def clear(self):
        self._session.clear()