# coding=utf-8

"""
.. module:: models
    :platform: appengine
    :synopsis: Modelo de Tag
"""


from django.utils.translation import gettext_lazy as _
from google.appengine.ext import db


SEPARATOR = ','
class TagHelper(object):
    def get_by_name(self, name):
        return Tag.get_by_key_name('tag_%s' % name.lower())
    
    def order_by_frequency(self):
        list = Tag.gql('WHERE count > 0 ORDER BY count DESC')


class Tag(db.Model):
    """Tag, el nombre se guarda tambien en el key_name, de la forma tag_name"""
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty(default=0)
    objects = TagHelper()
    
    @staticmethod
    def __key_name(name):
        return 'tag_%s' % name.lower()
    
    @classmethod
    def get_or_insert(cls, key_name=None, **kwargs):
        """USE THIS METHOD TO CREATE A NEW TAG, USE KEY_NAME = None"""
        if kwargs['name'] is None or kwargs['name'] == '':
            return None
        if key_name is None:
            key_name = Tag.__key_name(kwargs['name'])
        tag = Tag.get_by_key_name(key_name)
        if tag is not None:
            return tag
        return super(Tag, cls).get_or_insert(key_name, **kwargs)
    
    @classmethod
    def desc_count(cls, key, value=1):
        def _tx(key, value):
            value = int(value)
            obj = Tag.get(key)
            if obj.count > 0:
                obj.count -= value
                obj.put()
        db.run_in_transaction(_tx, key, value)
    
    @classmethod        
    def inc_count(cls, key, value=1):
        def _tx(key, value):
            value = int(value)
            obj = Tag.get(key)
            obj.count += value
            obj.put()
        db.run_in_transaction(_tx, key, value)
        
    def __str__(self):
        return unicode(self.name).encode('utf-8')

    def __unicode__(self):
        return self.name


class Taggable(db.Model):
    """
        Para acceder a los atributos de aqui en una clase hijo de esta,
        hay que poner __Tagabble antes del atributo.
        usar: object.__Tagabble__tags_list
    """
    _tags_list = db.ListProperty(db.Key, default=[])
    __tags = None
    __tags_named = None
    
    @property
    def _tags(self):
        """Lee la lista de tags y devuelve las instancias"""
        if self.__tags is None:
            from google.appengine.api import datastore
            self.__tags = datastore.Get(self._tags_list)
        return self.__tags
    
    @property
    def tags(self):
        if self.__tags_named is None:
            self.__tags_named =  [tag['name'] for tag in self._tags]
        return self.__tags_named
        
    def _tags_setter(self, tags, commit=True):
        from types import UnicodeType, StringType, ListType
        """Crea la lista o añade el tag"""
        if type(tags) is StringType:
            tags = unicode(tags)
        if type(tags) is UnicodeType:
            tags = tags.split(SEPARATOR)
        if type(tags) is ListType:
            tags = [t.strip().lower() for t in tags]
            for tag in tags:  # recorremos toda la lista de tags y añadirmos los que sean nuevos
                tagInstance = Tag.get_or_insert(name=tag)
                if tagInstance is not None and not tagInstance.key() in self._tags_list:
                    self._tags_list.append(tagInstance.key())
                    Tag.inc_count(tagInstance.key())
            if commit:
                self.put()
        else:
            raise AttributeError
