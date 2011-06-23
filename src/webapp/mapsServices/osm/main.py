# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.


"""
from OSMRequest import *
import urllib2
import sys    
    
def run():
    
    response, content = OSMRequest.get_capabilities()
    
    
    print OSMResponse.from_response(response).xml.write(sys.stdout)
    
    response = OSMRequest.retrieve_hospitals(lat=-3.5978214, lon=37.176107)
    
    
    r = OSMResponse.from_response(response)
    from xml.etree import ElementTree
    print r.nodes
    
if __name__ == '__main__':
    run()
    print 'Done.'
