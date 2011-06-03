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
import os
version = os.environ["CURRENT_VERSION_ID"]
#===============================================================================
# About memcache: http://blog.notdot.net/2009/9/Efficient-model-memcaching
#===============================================================================
from google.appengine.api import memcache 
from google.appengine.ext import db 
from google.appengine.datastore import entity_pb



def serialize_instances(instances):
    """
        Serializes the data before saving it in the memcache
    """
    if instances is None:
        return None
    elif isinstance(instances, db.Model):
        return db.model_to_protobuf(instances).Encode()#instances is only one
   
    return [db.model_to_protobuf(x).Encode() for x in instances]

def deserialize_instances(data):
    """
        Get and deserializes the data from the cache, return a instance of the model
    """
    if data is None:
        return None
    elif isinstance(data, str):
        return db.model_from_protobuf(entity_pb.EntityProto(data))#just one instance in data
    
    return [db.model_from_protobuf(entity_pb.EntityProto(x)) for x in data]#data contains a list of objects

    
    