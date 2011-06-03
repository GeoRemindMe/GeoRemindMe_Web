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

import random
from google.appengine.ext import db
from google.appengine.api import memcache

#===============================================================================
# info: http://code.google.com/intl/es-ES/appengine/articles/sharding_counters.html
#===============================================================================

SHARDS = 5

class RouteCounter(db.Model):
    instance = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)
    
    @classmethod
    def get_count(cls, instance):
        '''
            Returns the value of the counter, is counters is not in memcache, 
            counts all the sharded counters
        ''' 
        instance=str(instance)
        total = memcache.get(instance)
        if not total:
            total = 0
            counters = RouteCounter.gql('WHERE instance = :1', instance)
            for counter in counters:
                total += counter.count
            memcache.add(instance, str(total), 60)
        return int(total)
    
    @classmethod
    def increase_counter(cls, instance):
        '''
            Increment the counter of given key
        '''
        instance=str(instance)
        def increase():
            index = random.randint(0, SHARDS-1)#select a random shard to increases
            shard_key = instance + str(index)#creates key_name
            counter = RouteCounter.get_by_key_name(shard_key)
            if not counter:#if counter doesn't exist, create a new one
                counter = RouteCounter(key_name=shard_key, instance=instance)
            counter.count +=1
            counter.put()
        db.run_in_transaction(increase)
        memcache.incr(instance, initial_value=0)
        
            