# coding=utf-8

"""
.. module:: funcs
    :platform: appengine
    :synopsis: Funciones comunes para todo el proyecto
"""


from django.utils import simplejson
from google.appengine.ext import db


class GqlEncoder(simplejson.JSONEncoder): 

    """Extends JSONEncoder to add support for GQL results and properties. 

    Adds support to simplejson JSONEncoders for GQL results and properties by 
    overriding JSONEncoder's default method. 
    """ 

    # TODO Improve coverage for all of App Engine's Property types. 

    def default(self, obj): 

        """Tests the input object, obj, to encode as JSON.""" 
        
        from datetime import datetime
        from time import mktime, struct_time
        from google.appengine.api import users
        if hasattr(obj, '__json__'): 
            return getattr(obj, '__json__')() 
        if isinstance(obj, db.GqlQuery): 
            return list(obj) 
        elif isinstance(obj, db.Model): 
            properties = obj.properties().items() 
            output = {} 
            for field, value in properties: 
                output[field] = getattr(obj, field) 
            return output 
        elif isinstance(obj, datetime): 
            output = {} 
            fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second', 'year'] 
            methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday', 'timetuple'] 
            for field in fields: 
                output[field] = getattr(obj, field) 
            for method in methods: 
                output[method] = getattr(obj, method)() 
            output['epoch'] = mktime(obj.timetuple()) 
            return output 
        elif isinstance(obj, struct_time): 
            return list(obj) 
        elif isinstance(obj, users.User): 
            output = {} 
            methods = ['nickname', 'email', 'auth_domain'] 
            for method in methods: 
                output[method] = getattr(obj, method)() 
            return output
        elif isinstance(obj, db.GeoPt):
            output = {}
            return output
        return simplejson.JSONEncoder.default(self, obj) 


def make_random_string(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        #"Generates a random string with the given length and given allowed_chars"
        # Note that default value of allowed_chars does not have "I" or letters
        # that look like it -- just to avoid confusion.
        
        # I take this from django.contrib.auth
        from random import choice
        return ''.join([choice(allowed_chars) for i in xrange(length)])

    
def u_slugify(txt):
        import re
        """A custom version of slugify that retains non-ascii characters. The purpose of this
        function in the application is to make URLs more readable in a browser, so there are 
        some added heuristics to retain as much of the title meaning as possible while 
        excluding characters that are troublesome to read in URLs. For example, question marks 
        will be seen in the browser URL as %3F and are thereful unreadable. Although non-ascii
        characters will also be hex-encoded in the raw URL, most browsers will display them
        as human-readable glyphs in the address bar -- those should be kept in the slug."""
        txt = txt.strip() # remove trailing whitespace
        txt = re.sub('\s*-\s*','-', txt, re.UNICODE) # remove spaces before and after dashes
        txt = re.sub('[\s/]', '_', txt, re.UNICODE) # replace remaining spaces with underscores
        txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE) # replace colons between numbers with dashes
        txt = re.sub('"', "'", txt, re.UNICODE) # replace double quotes with single quotes
        txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]ñ','',txt, re.UNICODE) # remove some characters altogether
        return txt
    

def prefetch_refprops(entities, *props):
    # from http://blog.notdot.net/2010/01/ReferenceProperty-prefetching-in-App-Engine
    """
        Carga todas las referencias de un grupo de objetos
        en una sola consulta al datastore
    """
    fields = [(entity, prop) for entity in entities for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]
    ref_keys = filter(None, ref_keys)
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    for (entity, prop), ref_key in zip(fields, ref_keys):
        if ref_key is not None:
            prop.__set__(entity, ref_entities[ref_key])
    return entities


def single_prefetch_refprops(entity, *props):
    # from http://blog.notdot.net/2010/01/ReferenceProperty-prefetching-in-App-Engine
    """
        Carga todas las referencias de un objeto
        en una sola consulta al datastore
    """
    fields = [(entity, prop) for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]
    ref_keys = filter(None, ref_keys)
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    for (entity, prop), ref_key in zip(fields, ref_keys):
        if ref_key is not None:
            prop.__set__(entity, ref_entities[ref_key])
    return entity


def fetch_parents(entities):
    # from http://blog.notdot.net/2010/01/ReferenceProperty-prefetching-in-App-Engine
    """
        Carga y devuelve la lista de parents
        directamente en una sola consulta al datastore
    """
    ref_keys = [x.parent_key() for x in entities if x.parent_key() is not None]
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    parents = []
    for entity in entities:
        parents.append(ref_entities[entity.parent_key()])
    return parents
