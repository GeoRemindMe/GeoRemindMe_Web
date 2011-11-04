# coding=utf-8

#
# Copyright 2011 Sahid Orentino Ferdjaoui.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""App Engine Model Plus is an abstract layer for db.Model.
It keeps the same comportment of db.Model but add a cache layer with memcached and
adds several methods to take it more efficient.

For the moment App Engine Model Plus overide 3 method of db.Model
db.put, db.get and db.delete, it also adds several methods:

  * prefetch, Largely inspired by the topic of Nick's Blog http://goo.gl/tU92
    this method retrieve every db.ReferenceProperty of your model.

  * ...

App Engine Model Plus help also to fine tune the comportment of your calls into
with the datastore. You can configure deadline, retry, and read policy.

To use it, simply you need to extend your model with it.

    class Story(mp.Model):
      title = db.StringProperty()
      body = db.TextProperty()
      created = db.DateTimeProperty(auto_now_add=True)

With this module i have trying to get the better part of async methods
found by db.Model to accomplish storage into memcached without pertube the
put to the datastore.

Publics methods found with appengine-model+:
    prefetch    - Prefetch every db.ReferenceProperty in a model or a list of models.
    serialize   - serialize a db.Model into protocol buffer.
    unserialize - unserialize protocol buffer model into db.Model.
    mp.get      - Keeps the same comportement of db.get but search firstely
                  to retrieve model(s) from memcached.
    mp.put      - Keeps the same comportement of db.put but store firtely the model(s)
                  into memcached.
    mp.delete   - Keeps the same comportement of db.delete but replace every
                  model(s) already stored in memcached by None.
"""

__author__ = 'sahid.ferdjaoui@gmail.com (Sahid Orentino Ferdjaoui)'

import logging
import time

try:
    import os
    version = os.environ["CURRENT_VERSION_ID"]
except KeyError:
    version = 1

from google.appengine.ext import db, search
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.runtime import apiproxy_errors


__all__ = ['put', 'get', 'delete',
           'serialize', 'unserialize', 'prefetch',
           'Model',]


DEBUG=False
"""DEBUG The debug status.
"""

DATASTORE_NB_RETRY=2
"""DATASTORE_NB_RETRY
Is the number of retries the method do.

TODO(sahid): Needs a better doc.
"""

DATASTORE_TIME_RETRY=.15
"""DATASTORE_TIME_RETRY
Is the time to the process waiting before try a new call.

TODO(sahid): Needs a better doc.
"""

DATASTORE_DEADLINE=5
"""DATASTORE_DEADLINE
Is the timeout of and datastore action.

TODO(sahid): Needs a better doc.
"""

DATASTORE_CONSISTENCY=db.STRONG_CONSISTENCY
"""DATASTORE_CONSISTENCY
Is the read policy.

  db.STRONG_CONSISTENCY
  db.EVENTUAL_CONSISTENCY

TODO(sahid): Needs a better doc.
"""

MEMCACHE_PREFIX='%sgae-model+' % version
"""MEMCACHE_PREFIX
The prefix used by memcache to store entities.

TODO(sahid): Needs a better doc.
"""

MEMCACHE_TIME=0
"""MEMCACHE_TIME
The expiration time in seconds

TODO(sahid): Needs a better doc.
"""

MEMCACHE_NAMESPACE=''
"""MEMCACHE_NAMESPACE
The namespace used by memcache

  /!\ Not implemented.

TODO(sahid): Needs a better doc.
"""

def debug(m):
    if DEBUG:
        logging.info(m)

def serialize(models):
    """Serializes a model or a lists in in a protobuf protocol
    TODO(sahid): Needs a better doc.

    TODO(sahid): Put the link.
    Notes:
      Largely inspired from Nick's blog
      
    Returns a model or a lists of models serialized in a protobuf protocol.
    """
    if models is None:
        return None
    elif isinstance(models, search.SearchableModel):
        return models._populate_entity(_entity_class=search.SearchableEntity)._ToPb() 
    elif isinstance(models, db.Model):
        return db.model_to_protobuf(models).Encode()#instances is only one
    elif isinstance(models, list):
        models = filter(None, models)
        return [serialize (x) for x in models]
    elif isinstance(models, dict):
        return dict([(k, serialize(x)) for k, x in models.items()])

def unserialize(data, _search_class=None):
    """
        Get and deserializes the data from the cache, return a instance of the model
    """
    if data is None:
        return None
    if _search_class is not None:
        if type(data) == type(list):
            return [unserialize(x, search_class=_search_class) for x in data]#data contains a list of objects
        return _search_class.from_entity(search.SearchableEntity.FromPb(data))
    if isinstance(data, basestring):
        return db.model_from_protobuf(datastore.entity_pb.EntityProto(data))
    elif isinstance(data, list):
        return [unserialize (x) for x in data]
    elif isinstance(data, dict):
        return dict([(k, unserialize(x)) for k, x in data.items()])


DATASTORE_CONFIG_WHITLIST=('deadline', 'read_policy')
def _cfg_kwargs(f):
    def wrapper(x, *args, **kwds):
        if not kwds.has_key('config'):
            if f.__name__ == 'get':
                params = {
                          'read_policy':DATASTORE_CONSISTENCY,
                          'deadline': DATASTORE_DEADLINE,}
            else:
                params = {
                          'deadline': DATASTORE_DEADLINE,}
            kwds['config'] = db.create_config(**params)
        return f(x, *args, **kwds)
    wrapper.__name__ = f.__name__
    return wrapper

def prefetch(entities, *props):
    """Returns...
    
    Notes:
      Largely inspired from Nick's blog (http://goo.gl/tU92)

    TODO(sahid): Needs a better doc.
    """
    multiple = isinstance(entities, list)
    
    if not multiple:
        entities = [entities]
    entities = filter(None, entities)
    if not any(entities):
        if multiple:
            return []
        return None
    if not props:
        props = [prop for key, prop in entities[0].properties().items()
                 if isinstance(prop, db.ReferenceProperty)]
        
    debug("props=%s" % ','.join(prop.__class__.__name__ for prop in props))
    if not props:
        return # nothings to do.
    
    fields = [(entity, prop) for entity in entities for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]
    ref_keys = filter(None, ref_keys)
    if any(ref_keys):
        # Because if ref_keys has a None value,
        # db.get raise a BadArgumentError exception.
        for (i, v) in enumerate (ref_keys):
            if v is None:
                del ref_keys[i]
                del fields[i]
    
        ref_entities = dict((x.key(), x) for x in get(set(ref_keys)) if x is not None)
    
        unreferenced = []
        for (entity, prop), ref_key in zip(fields, ref_keys):
            if ref_key in ref_entities:
                prop.__set__(entity, ref_entities[ref_key])
            else:
                logging.warn("Reference invalide: %s" % entity)
                unreferenced.append(entity.key ())
                try:
                    entities.remove (entity)
                except ValueError:
                    logging.warn("Very weird %s not in %s" % (entities, entity))
    
        if unreferenced:
            logging.warn("These keys are references invalide into the datastore: %s" % unreferenced)
    
        if multiple:
            return entities
        return entities[0]
    
    
def fetch_parentsKeys(entities):
    # from http://blog.notdot.net/2010/01/ReferenceProperty-prefetching-in-App-Engine
    """
        Carga y devuelve la lista de parents
        directamente en una sola consulta al datastore
    """
    ref_keys = [x.parent() for x in entities]
    return get(set(ref_keys))


old_db_put = db.put
@_cfg_kwargs
def put(models, **kwargs):
    """Store one or more Model instance, every stored
    models are pushed also into memcache.

    TODO(sahid): Needs a better doc.
    """
    memclient = memcache.Client()
    for retry in xrange(DATASTORE_NB_RETRY):
        try:
            models, multiple = datastore.NormalizeAndTypeCheck(models, db.Model)
            if not any(models): return multiple and [] or None # Nothings to do.
            async = db.put_async(models, **kwargs)
            try:
                debug("Needs to put models=%s" % ','.join(m.__class__.__name__ for m in models))
                #TODO(sahid): Needs factorization.
                k = [unicode(x.key()) for x in models]
                v = serialize(models)
                memclient.set_multi(dict(zip(k, v)),
                                   time=MEMCACHE_TIME,
                                   key_prefix=MEMCACHE_PREFIX)
                ret = async.get_result()
            except datastore_errors.BadKeyError:
                debug("Incomplete key passed, "
                      "can't store in memcached before put in the datastore.")
                # Incomplete key
                # It's better to use key_name with mp.
                ret = async.get_result()
                if ret:
                    k = map(unicode, ret)
                    v = serialize(models)
                    memclient.set_multi(dict(zip(k, v)),
                                       time=MEMCACHE_TIME,
                                       key_prefix=MEMCACHE_PREFIX)
            if multiple:
                return ret
            return ret[0]
        except (db.Timeout,
                db.TransactionFailedError,
                apiproxy_errors.ApplicationError,
                apiproxy_errors.DeadlineExceededError), e:
            logging.warn("Error during the put process, "
                         "retry %d in %.2fs", retry, DATASTORE_TIME_RETRY)
            logging.debug(e.message)            
            time.sleep(DATASTORE_TIME_RETRY)
        logging.exception(e)
db.put=put


@_cfg_kwargs
def get(keys, **kwargs):
    """Fetch the specific Model instance with the given key from the datastore.

    TODO(sahid): Needs a better doc.
    """
    memclient = memcache.Client()
    for retry in xrange(DATASTORE_NB_RETRY):
        
            keys, multiple = datastore.NormalizeAndTypeCheckKeys(keys)
            if not any(keys): return multiple and [] or None # Nothings to do.
            
            keys = set(map(unicode, keys))
            debug("Needs to retrieved keys=%s" % keys)
            ret=[]
            # First checks keys already in memcached.
            in_mem = memclient.get_multi(keys, key_prefix=MEMCACHE_PREFIX)
            debug('dict=%s' % in_mem)
            ret.extend(unserialize(in_mem.values()))
            debug("in_mem=%s" % in_mem.keys())
            keys = keys.difference(in_mem.keys())
            if keys:
                in_db = db.get(keys, **kwargs)
                ret.extend(in_db)
                # We now add every not cached model in memache.
                # TODO(sahid): Maybe we can factorized this part of code
                # with put().
                #k = [x and unicode(x.key()) or None for x in in_db]
                debug("in_db=%s, k=%s" % (in_db, keys))
                v = serialize(in_db)
                memclient.add_multi(dict(zip(keys, v)),
                                   time=MEMCACHE_TIME,
                                   key_prefix=MEMCACHE_PREFIX)
            if multiple:
                return ret
            return ret[0]
        
        
    

@_cfg_kwargs
def delete(models, **kwargs):
    """Delete one or more Model instances.

    Note: db.get returns None of the key doesn't exits
    so we can replace in memcache every deleted keys by None.

    TODO(sahid): Needs a better doc.
    """
    memclient = memcache.Client()
    for retry in xrange(DATASTORE_NB_RETRY):
        try:
            keys, multiple = datastore.NormalizeAndTypeCheckKeys(models)
            if not any(keys): return multiple and [] or None # Nothings to do.
            
            async = db.delete_async(models, **kwargs)
            mapping = dict((unicode(k), None) for k in keys)
            
            memclient.replace_multi(mapping,
                                   time=MEMCACHE_TIME,
                                   key_prefix=MEMCACHE_PREFIX)
            return async.get_result()
        except (db.Timeout,
                db.TransactionFailedError,
                apiproxy_errors.ApplicationError,
                apiproxy_errors.DeadlineExceededError), e:
            logging.warn("Error during the delete process, "
                         "retry %d in %.2fs", retry, DATASTORE_TIME_RETRY)
            logging.debug(e.message)            
            time.sleep(DATASTORE_TIME_RETRY)
    logging.exception(e)

    
class Model(db.Model):
    """A Model extends db.Model.

    TODO(sahid): Needs doc.
    """
    
    def put(self, **kwargs):
        """Writes this model instance to the datastore.
        Keeps the same comportement of db.Model.put()

        TODO(sahid): Needs doc.
        """
        self._populate_internal_entity()
        return put(self, **kwargs)

    def delete(self, **kwargs):
        """Deletes this entity from the datastore.
        Keeps the same comportement of db.Model.delete()

        TODO(sahid): Needs doc.
        """
        delete(self.key(), **kwargs)

        self._key = self.key()
        self._key_name = None
        self._parent_key = None
        self._entity = None

    def prefetch(self, *props):
        """Prefetch all db.ReferenceProperty of this model.

        TODO(sahid): Needs doc.
        """
        prefetch(self, *props)

    @classmethod
    def get(cls, keys, **kwargs):
        """Fetch instance from the datastore of a specific Model type using key.
        Keeps the same comportement of db.Model.get()
        
        TODO(sahid): Needs doc.
        """
        results = get(keys, **kwargs)
        if results is None:
            return None
        if isinstance(results, db.Model):
            instances = [results]
        else:
            instances = results

        for instance in instances:
            if not(instance is None or isinstance(instance, cls)):
                raise db.KindError('Kind %r is not a subclass of kind %r' %
                                (instance.kind(), cls.kind()))
        return results

    @classmethod
    def get_by_key_name(cls, key_names, parent=None, **kwargs):
        """Get instance of Model class by its key's name.
        Keeps the same comportement of db.Model.get_by_key_name()
        
        TODO(sahid): Needs doc.
        """
        try:
            parent = db._coerce_to_key(parent)
        except db.BadKeyError, e:
            raise db.BadArgumentError(str(e))
        key_names, multiple = datastore.NormalizeAndTypeCheck(key_names, basestring)
        keys = [datastore.Key.from_path(cls.kind(), name, parent=parent)
                for name in key_names]
        ret = get(keys, **kwargs)
        if multiple:
            return ret
        return ret[0]

    @classmethod
    def get_by_id(cls, ids, parent=None, **kwargs):
        """Get instance of Model class by id.
        Keeps the same comportement of db.Model.get_by_id()
        
        TODO(sahid): Needs doc.
        """
        if isinstance(parent, db.Model):
            parent = parent.key()
        ids, multiple = datastore.NormalizeAndTypeCheck(ids, (int, long))
        keys = [datastore.Key.from_path(cls.kind(), id, parent=parent)
                for id in ids]
        ret = get(keys, **kwargs)
        if multiple:
            return ret
        return ret[0]
    
    def _pre_put(self):
        pass

    def _post_put(self):
        pass
    
    def _post_put_sync(self, **kwargs):
        pass
    
    def _pre_delete(self):
        pass
    
    def _post_delete(self):
        pass
    
    def put_async(self,**kwargs):
        return db.put_async(self)
    
    def delete_async(self):
        return db.delete_async(self)


old_async_put = db.put_async
def hokked_put_async(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, Model):
            debug("pre_put_async")
            model._pre_put()
    async = old_async_put(models, **kwargs)
    debug("put_async")
    get_result = async.get_result
    def get_result_with_callback():
        for model in models:
            if isinstance(model, Model):
                model._post_put()
        return get_result()
    async.get_result = get_result_with_callback
    debug("end_put_async")
    return async
db.put_async = hokked_put_async


old_async_delete = db.delete_async
def hokked_delete_async(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, Model):
            debug("pre_delete_async=%s" % model)
            model._pre_delete()
    async = old_async_delete(models, **kwargs)
    debug("delete_async=%s" % models)
    get_result = async.get_result
    def get_result_with_callback():
        for model in models:
            if isinstance(model, Model):
                model._post_delete()
        return get_result()
    async.get_result = get_result_with_callback
    debug("post_delete_async=%s" % models)
    return async
db.delete_async = hokked_delete_async


old_put = db.put
def hokked_put(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, Model):
            debug("pre_put")
            model._pre_put()
        old_put(models, **kwargs)
        debug("put")
        if isinstance(model, Model):
            model._post_put_sync(**kwargs)
            debug("post_put")
db.put = hokked_put


old_delete = db.delete
def hokked_delete(models, **kwargs):
    if type(models) != type(list()):
        models = [models]
    for model in models:
        if isinstance(model, Model):
            debug("pre_delete")
            model._pre_delete()
        old_delete(model, **kwargs)
        debug("delete")
        if isinstance(model, Model):
            model._post_delete()
            debug("post_delete")
db.delete = hokked_delete


