# coding=utf-8

import libs.httplib2 as httplib2
from xml.etree import ElementTree
from google.appengine.api.memcache import Client


def _get_bbox(lat, lon):
    '''
        creates the bbox needed for the queries
    '''
    final = [lat-0.5, lon-0.5,lat+0.5,lon+0.5]
    final = [('%.8f' % float(p)) for p in final]
    return ','.join(final)

class OSMAPIError(Exception):
    def __init__(self, type, message=''):
        Exception.__init__(self, message)
        self.type = type

class OSMResponse(object):
    '''
        Class for parsing the XML response from openstreetmaps
    '''
    def __init__(self, xml):
        self.xml = xml
        self._nodes = self.xml.findall("node")
        self.nodes = dict()
        i = 0
        for node in self._nodes:
            self.nodes['%d' % i] = {
                                          'id' :node.attrib['id'],
                                          'lat':node.attrib['lat'], 'lon':node.attrib['lon'],
                                          'timestamp': node.attrib['timestamp'],
                                          'changeset': node.attrib['changeset'],
                                          }
            tags = node.findall("tag")
            for tag in tags:
                self.nodes['%d' % i].update({tag.attrib['k']: tag.attrib['v']})
            i += 1

    @classmethod
    def from_response(cls, response=None):
        xml = ElementTree.parse(response)
        return OSMResponse(xml=xml)
    
class OSMRequest(httplib2.Http):
    '''
        encapsulates the queries
    '''
    #_base_url = 'http://api.openstreetmap.org/'
    #_base_url = 'http://api06.dev.openstreetmap.org/'
    _base_url = 'http://jxapi.openstreetmap.org/xapi/api/0.6/'
    headers = { 'User-Agent' : 'Georemindme v.0.1 - georemindme.appengine.com' }
    
    def __init__(self, *args, **kwargs):
        mem = Client()
        super(OSMRequest, self).__init__(cache=mem, timeout=10, *args, **kwargs)
    
    def get_capabilities(self):
        url = self._base_url + 'capabilities'
        response, content = self.request(url, method='GET')
        if response['status'] != 200:
            raise OSMAPIError(response['status'], content)
        return content
        
    
    def retrieve_shops(self, lat, lon):
        pos = _get_bbox(lat, lon)
        return self._retrieve_nodes(pos, type='shop')
    

    def retrieve_hospitals(self, lat, lon):
        pos = _get_bbox(lat, lon)
        return self._retrieve_nodes(pos, value='hospital')
    
    def _retrieve_nodes(self, pos, type='amenity', value='*'):
        url = self._base_url + 'node[%s=%s][bbox=%s]' % (type, value, pos)
        print url
        response, content = self.request(url, method='GET', headers=self.headers)
        if response['status'] != 200:
            raise OSMAPIError(response['status'], content)
        return content
    

    
