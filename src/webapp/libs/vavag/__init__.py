# coding=utf-8

__author__ = "Javier Cordero Martinez (javier@georemindme.com)"
__copyright__ = "Copyright 2011"
__contributors__ = []
__license__ = "AGPLv3"
__version__ = "0.1"
"""
    Vavag python client
    Copyright (C) 2011  Javier Cordero Martinez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from libs.httplib2 import Http
# http://vavag.com/help/api/v2


class VavagException(Exception):
    status = None
    msg = None
    def __init__(self, status, msg):
        super(self.__class__, self).__init__()
        self.status = status
        self.msg = msg


class VavagRequest(Http):
    headers = { 'User-Agent' : 'Vavag python: %s' % __version__ }
    URL_get_info_url = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/get_info_url?url='
    URL_get_pack = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/get_pack?packhash='
    URL_set_pack = 'http://vavag.com/api/%(version)s/%(method)s/%(login)s/%(apikey)s/set_pack?packchain='
    
    def __init__(self, login, api_key, version='v2', method = 'json', **kwargs):
        super(self.__class__, self).__init__(timeout=20, **kwargs)
        self.version = version
        self.api_key = api_key
        self.login = login
        self.method = method

    def _encode(self, url):
        from urllib import quote
        if not 'http://' in url and not 'https://' in url:
            url = 'http://' + url
        return quote(url)
        #from base64 import urlsafe_b64encode
        #return urlsafe_b64encode(url)
    
    def get_info(self, url):
        request_url = self.URL_get_info_url % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        request_url = request_url + self._encode(url)
        return self._do_request(request_url)
    
    def get_pack(self, packHash):
        request_url = self.URL_get_pack % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        request_url = request_url + packHash
        return self._do_request(request_url)
    
    def set_pack(self, pack):
        """
            Creates a new pack of urls
        """
        request_url = self.URL_set_pack % {
                                       'version': self.version,
                                       'method': self.method,
                                       'login': self.login,
                                       'apikey': self.api_key
                                       }
        
        if type(pack) != type(list()):
            type_param = 2
        else:
            type_param = 1
            pack = '|sep|'.join([self._encode(url) for url in pack])
        request_url = request_url + pack + '&type=%s' % type_param
        return self._do_request(request_url)
    
    def _do_request(self, url, method='GET', body=None):
        """
            Does a request:
            
                :param url: url to request
                :type url: string
                :returns: dict with the results from vavag.com
                :raises: :class:`VavagException`
        """
        response, content = self.request(url, method=method, body=body, headers=self.headers)
        if response['status'] != 200:
            raise VavagException(status=response['status'], msg='ERROR IN REQUEST')
        from django.utils import simplejson
        json = simplejson.loads(content)
        if json['status'] == 200:
            return json['results']
        raise VavagException(status=json['status'], msg=json['statusMsg'])
