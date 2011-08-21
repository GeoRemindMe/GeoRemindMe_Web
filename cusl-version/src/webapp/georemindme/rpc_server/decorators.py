from jsonrpcserver import jsonrpc_function

from models import UserRPC

from exceptions import *


def jsonrpc_logged_function(func, *args, **kwargs):

    def _wrapper(*args, **kwargs):
        if 'session_id' in kwargs:
            urpc = UserRPC.get_by_id(kwargs['session_id'])
            if urpc is not None and urpc.is_valid():
                return func(*args, **kwargs)
        
        raise LoginException("User not logged")
    
    return _wrapper
