# coding=utf-8

import libs.httplib2 as httplib2
from xml.etree import ElementTree
from google.appengine.api.memcache import Client


def _get_bbox(lat, lon):
    '''
        creates the bbox needed for the queries
    '''
    final = [lat-0.2, lon-0.2,lat+0.2,lon+0.2]
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
    _base_url = 'http://open.mapquestapi.com/xapi/api/0.6/'
    #_base_url = 'http://jxapi.openstreetmap.org/xapi/api/0.6/'
    headers = { 'User-Agent' : 'Georemindme:0.1' }
    
    def __init__(self, *args, **kwargs):
        mem = Client()
        super(OSMRequest, self).__init__(cache=mem, timeout=20, *args, **kwargs)
    
    def get_capabilities(self):
        url = self._base_url + 'capabilities'
        response, content = self.request(url, method='GET')
        if response['status'] != 200:
            raise OSMAPIError(response['status'], content)
        return content
        
    def retrieve_id(self, id):
        url = self._base_url + 'node/%s' % id
        
    
    def retrieve_shops(self, lat, lon, type='*'):
        bbox = _get_bbox(lat, lon)
        url = self._base_url + 'node[shop=*][bbox=%s]' % bbox
        return self._retrieve_nodes(url)
    

    def retrieve_hospitals(self, lat, lon):
        return self._retrieve_amenity(lat, lon, 'hospital')
    
    
    def retrieve_restaurants(self, lat, lon):
        return self._retrieve_amenity(lat, lon, 'restaurant')
               
    
    def _retrieve_nodes(self, url):
        response, content = self.request(url, method='GET', headers=self.headers)
        if response['status'] != 200:
            raise OSMAPIError(response['status'], content)
        return content
    
    
    def _retrieve_amenity(self, lat, lon, name):
        bbox = _get_bbox(lat, lon)
        url = self._base_url + 'node[amenity=%s][bbox=%s]' % (name, bbox)
        return self._retrieve_nodes(url) 
        
    

        
    

    
