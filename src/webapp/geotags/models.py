# coding=utf-8

from types import UnicodeType, StringType, ListType
from string import split
from google.appengine.ext import db, search

SEPARATOR = ','

class TagHelper(object):
    def get_by_name(self, name):
        return Tag.get_by_key_name(Tag.__key_name(name))
    
    def order_by_frequency(self):
        list = Tag.gql('WHERE count > 0 ORDER BY count DESC')

class Tag(search.SearchableModel):
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    count = db.IntegerProperty(default=0)
    objects = TagHelper()
    
    @staticmethod
    def __key_name(name):
        return 'tag_%s' % name
    
    @classmethod
    def get_or_insert(cls, key_name=None, **kwargs):
        """USE THIS METHOD TO CREATE A NEW TAG, USE KEY_NAME = None"""
        if key_name is None:
            key_name = Tag.__key_name(kwargs['name'])
        tag = Tag.get_by_key_name(key_name)
        if tag is not None:
            return tag
        super(Tag, cls).get_or_insert(key_name, **kwargs)
    
    def desc_count(self, value=1):
        def _tx(value):
            self.count -= value
            self.put()
        db.run_in_transaction(_tx)
            
    def inc_count(self, value=1):
        def _tx(value):
            self.count += value
            self.put()
        db.run_in_transaction(_tx)

class Taggable(db.Model):
    '''
        Para acceder a los atributos de aqui en una clase hijo de esta,
        hay que poner __Tagabble antes del atributo.
        usar: object.__Tagabble__tags_list
    '''
    __tags_list = db.ListProperty(db.Key)
    __tags = None
    
    @property
    def _tags(self):
        """Lee la lista de tags y devuelve las instancias"""
        if self.__tags_list is None or len(self.__tags_list) == 0:
            return None
        self.__tags = Tag.get(self.__tags_list)
        return self.__tags
    
    def _tags_setter(self, tags):
        """Crea la lista o añade el tag"""
        if type(tags) is UnicodeType:
            tags = str(tags)
        if type(tags) is StringType:
            tags = split(tags, SEPARATOR)
        if type(tags) is ListType:
            self._tags()  # carga todos los tags existentes en una lista
            for tag in self.__tags:
                if tag not in tags:  #  un tag ya no esta en la lista nueva, lo borramos
                    self._remove_tag(tag)
            for tag in tags:  # recorremos toda la lista de tags y añadirmos los que sean nuevos
                if tag not in self.__tags:
                    self._add_tag(tag)
        else:
            raise Exception()
    _tags = property(_tags, _tags_setter)
        
    def _remove_tag(self, tag):
        tagInstance = Tag.objects.get_by_name(tag)
        if tag is None:
            return
        self.__tags.remove(tag)
        self.__tags_list.remove(tagInstance)
        tagInstance.desc_count()
        
    def _add_tag(self, tag):
        tagInstance = Tag.get_or_insert(tag)
        if tagInstance is None:
            return
        self.__tags_list.append(tagInstance)