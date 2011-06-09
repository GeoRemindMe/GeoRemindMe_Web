import uuid
from jsonrpc._json import loads, dumps
from jsonrpc.types import *
try:
    #raise Exception
    import urllib2
    from urllib2 import HTTPError
except:
    import urllib as urllib2
    class HTTPError(IOError):
        pass

class ServiceProxy(object):
  def __init__(self, service_url, service_name=None, version='1.0', timeout=None, secret=None):
    self.__version = str(version)
    self.__service_url = service_url
    self.__service_name = service_name
    self.__timeout = timeout
    self.__secret = secret

  def __getattr__(self, name):
    if self.__service_name != None:
      name = "%s.%s" % (self.__service_name, name)
    return ServiceProxy(self.__service_url, name, self.__version, timeout=self.__timeout, secret=self.__secret)
  
  def __repr__(self):
    return {"jsonrpc": self.__version,
            "method": self.__service_name}
  
  def __call__(self, *args, **kwargs):
    params = kwargs if len(kwargs) else args
    if Any.kind(params) == Object and self.__version not in ['2.0']:
      raise Exception('Unsupport arg type for JSON-RPC 1.0 '
                     '(the default version for this client, '
                     'pass version="2.0" to use keyword arguments)')
    # req = urllib2.Request(self.__service_url, )
    try:
        # 1. Prepare data
        url = self.__service_url
        data = dumps({
                      "jsonrpc": self.__version,
                      "method": self.__service_name,
                      'params': params,
                      'id': str(uuid.uuid1())})

        # 2. Sign it
        if self.__secret!=None:
            secret_key = callable(self.__secret) and self.__secret or self.__secret
            try: 
               from hashlib import md5
            except ImportError:
               from md5 import md5
            import urlparse
            from urllib import urlencode

            hash_code = md5(data+secret_key).hexdigest()
            url = list(urlparse.urlparse(url))
            params = dict([part.split('=') for part in url[4].split('&') if '&' in url[4]])
            params['hash_code'] = hash_code
            url[4] = urlencode(params)
            url = urlparse.urlunparse(url)

        # 3. Invoke RPC method
        if url.startswith('http://testserver/'):

            # 3.1 Using Django test client
            url = url.partition('http://testserver')[-1]
            from django.test import Client
            c = Client()
            r = c.post(url, content_type='application/x-www-form-urlencoded',data=data).content
        else:

            # 3.2 Using real HTTP connection
            if self.__timeout and urllib2.__name__ == 'urllib2':
                # Timeout is provided
                r = urllib2.urlopen(url, data, timeout=self.__timeout).read()
            else:
                # Timeout not provied, or not supported
                r = urllib2.urlopen(url, data).read()

        # 4. Load JSON
        y = loads(r)
    except HTTPError, e:
        r = None
        try:
            r = e.fp.read()
            y = loads(r)
        except Exception, e1:
            if r:
                raise Exception(r[:2000])
            raise e
    #except IOError, e:
    #   TODO: Never raise error

    # Dump error
    if y.get(u'error'):
      try:
        from django.conf import settings
        if settings.DEBUG:
            print '%s error %r' % (self.__service_name, y)
      except:
        pass
    return y
