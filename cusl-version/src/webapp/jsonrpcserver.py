"""
This Django middleware suits for building JSON-RPC servers.
Configuration:
    1) put class 'jsonrpcserver.JSONRPCServerMiddleware' to Django middleware list in settings.py
    2) add 'jsonrpc_urlpatterns' to 'urls.py' with 'urlpatterns' syntax
        example: 
            jsonrpc_urlpatterns = patterns('',
                (r'^myapp/json_rpc_service/$', 'myapp.newapp.json_rpc_views'),
                (r'^myapp/json_rpc_geoservice/$', 'myapp.geo.json_rpc_views'),
            )
        note: 'myapp.newapp.json_rpc_views' IS NOT A FUNCTION, BUT A MODULE, that
        contains exposed JSON-RPC functions.
    3) optional Django settings:
        1. JSONRPC_URLPATTERNS_NAME:
            Default value: 'jsonrpc_urlpatterns'.
            Name of the variable in urls.py,that contains JSON-RPC URL patterns.
            URL pattern must have Django syntax, but they must contain 
            MODULES NAMES, NOT FUNCTION NAMES as second element in tuple for patterns function.
        2. JSONRPC_SERIALIZER:
            Default value: JSONSerializer class - thin wrapper over django.utils.simplejson.
            Name of the JSON serializer class, that must have methods 
            'serialize' and 'deserialize'
        3. JSONRPC_JSONFY_AT_ALL_COSTS:
            Default value: False.
            Boolean flag, that determines whether JSON encoder should throwing an error or
            returning a str() representation of unsupportable python object.
            See implementation of AugmentedJSONEncoder class.
Use:
    1) write exposed functions:
        from jsonrpcserver import jsonrpc_function
        @jsonrpc_function
        def my_python_method(par1, par2):
            return par1 + par2
        ...
    2) use from JS client (e.g. dojo):
        var  service = new dojo.rpc.JsonService({
            "serviceType": "JSON-RPC", 
            "serviceURL": "/myapp/json_rpc_service/"
        });
        service.callRemote("my_python_method", ["string1", "string2"])
            .addCallback(...);
Specifications (json-rpc.org):
    input: '{"method":"my_python_method", "params": ["hello ", "world"], "id": 1}'
    output: '{"error": null, "result": "hello world", "id": 1}'

Written by alx3 (alx3apps(at)gmail(dot)com).
Inspired by Java Struts2 JSON-plugin by Musachy Barroso and
SimpleJSONRPCServer by David McNab.
You can use this code under the terms of BSD licence (like Django project).
"""

import sys
import traceback
import django
from django.http import HttpResponse
import django.utils.simplejson as json


_dispatchers_dict = {}

def _import_module(mod_name):
    """
    Importing module through __import__ function
    """
    module =  __import__(mod_name)
    components = mod_name.split('.')
    for comp in components[1:]:
        module = getattr(module, comp)
    return module

def _import_class(class_path):
    """
    Importing class through __import__ function
    """
    path_list = class_path.split(".")
    module_path = ".".join(path_list[:-1])
    class_name = path_list[-1]
    module = _import_module(module_path)
    return getattr(module, class_name)

class AugmentedJSONEncoder(json.JSONEncoder):
    """
    Augmentation for simplejson encoder.
    Now additionally encodes arbitrary iterables, class instances and decimals.
    """
#   switch this flag to True in production    
    if hasattr(django.conf.settings, "JSONRPC_JSONFY_AT_ALL_COSTS"):
        _jsonfy_at_all_costs_flag = django.conf.settings.JSONRPC_JSONFY_AT_ALL_COSTS;
    else:
        _jsonfy_at_all_costs_flag = False;

    def default(self, o):
        if(hasattr(o, 'isoformat')):
            return o.isoformat()
        if(hasattr(o, "__iter__")):
            iterable = iter(o)
            return list(iterable)
        elif(hasattr(o, "__add__") and hasattr(o, "__sub__") and hasattr(o, "__mul__")):
            return float(o)
        elif(hasattr(o, "__class__")):
            return o.__dict__
        else:
            if _jsonfy_at_all_costs_flag:
                return str(o)
            else:
#               JSON exception raised here                
                return json.JSONEncoder.default(self, o)

class JSONSerializer:
    """
    JSON encoder/decoder wrapper
    """
    def serialize(self, obj):
        return AugmentedJSONEncoder().encode(obj)
    def deserialize(self, string):
        return json.JSONDecoder().decode(string)


class FunctionDispatcher(object):
    """
    Simple function dispatcher.
    Dispatch syntax:
    result = disp.dispatch("my_fun", *["param1", param2])
    """
    def __init__(self):
        self.func_dict = {}

    def register_function(self, func, func_name=None):
        if not func_name:
            func_name = func.func_name
        #prevent overriding existing function
        if(self.func_dict.has_key(func_name)):
            raise Exception("Function '%s' already registered" % func_name)
        self.func_dict[func_name] = func

    def has_function(self, func_name):
        return func_name in self.func_dict

    def dispatch(self, func_name, *args, **kwargs):
        if func_name in self.func_dict:
            sought_func = self.func_dict[func_name]
        else:
            raise Exception("Function '%s' doesn't exist" % func_name)
        response = sought_func(*args, **kwargs)
        return response

def jsonrpc_function(func):
    """
    Decorator for JSON-RPC method.
    Server use:
        @jsonrpc_function
        def my_python_method(s1, s2):
            return s1 + s2;
    Client use (dojo):
        rpcService.callRemote("my_python_method", ["string1", "string2"])
            .addCallback(...);
    """
    if not _dispatchers_dict.has_key(func.__module__):
        _dispatchers_dict[func.__module__] = FunctionDispatcher()
    dispatcher = _dispatchers_dict[func.__module__]
    if not dispatcher.has_function(func.func_name):
        dispatcher.register_function(func)
    return func

class JSONRPCServerMiddleware(object):
    
    """
    Django middleware class. Put it Django middleware list in settings.py.
    """
    #searching for JSON-RPC urlpatterns 
    urls_mod_name = django.conf.settings.ROOT_URLCONF
    urls_module = _import_module(urls_mod_name)
    if hasattr(django.conf.settings, "JSONRPC_URLPATTERNS_NAME"):
        urlpatterns_name = django.conf.settings.JSONRPC_URLPATTERNS_NAME
    else:
        urlpatterns_name = "jsonrpc_urlpatterns" 
    jsonrpc_urlpatterns = getattr(urls_module, urlpatterns_name)

    def __init__(self):
        """
        Importing all modules, listed in jsonrpc_urlpatterns in urls.py.
        Initialization needs for fill dispatchers with funcitons.
        """
        for pattern in self.jsonrpc_urlpatterns:
            #django hack here, see django.core.urlresolvers.RegexUrlPattern class
            module_name = pattern._callback_str
            __import__(module_name)
        #initializing serializer
        if hasattr(django.conf.settings, "JSONRPC_SERIALIZER"):
            serializer_class = _import_class(django.conf.settings.JSONRPC_SERIALIZER)
            self.serializer = serializer_class()
        else:
            self.serializer = JSONSerializer()


    def process_request(self, request):
        """
        Preprocesses all POST request to find out whether its remote call.
        Processes remote call and returns HttpResponse as result
        """
        if(request.method == "GET"):
            return
        for pattern in self.jsonrpc_urlpatterns:
            match = pattern.regex.search(request.path[1:])
            if match:
                # If there are any named groups, use those as kwargs, ignoring
                # non-named groups. Otherwise, pass all non-named arguments as
                # positional arguments.
                kwargs = match.groupdict()
                if kwargs:
                    args = ()
                else:
                    args = match.groups()
                # In both cases, pass any extra_kwargs as **kwargs.
                kwargs.update(pattern.default_args)
                result_str = self._dispatch_rpc_call(pattern._callback_str, request.raw_post_data, args, kwargs)
                return HttpResponse(result_str)

    def _dispatch_rpc_call(self, module_name, raw_post_data, args, kwargs):
        response_dict = {}
        try:
            if module_name in _dispatchers_dict:
                dispatcher = _dispatchers_dict[module_name]
            else:
                raise Exception("Module '%s' doesn't have JSON-RPC functions" % module_name)

            call_data = self.serializer.deserialize(raw_post_data)
            call_id = call_data.get("id", None)
            if call_id:
                response_dict["id"] = call_id
            else:
                #following JSON-RPC spec, it's a notification, not a request 
                return ""
            func_name = str(call_data["method"])
            func_params = list(call_data["params"])

            args_list = list(args)
            args_list.extend(func_params)
            result = dispatcher.dispatch(func_name, *args_list, **kwargs)
            response_dict['result'] = result
            response_dict['error'] = None
        except Exception, e:
            error_dict = {
                    "name": str(sys.exc_info()[0]),
                    "message": str(e),
                    "stack": traceback.format_exc()
            }
            response_dict['error'] = error_dict
            response_dict['result'] = None
        return self.serializer.serialize(response_dict)


