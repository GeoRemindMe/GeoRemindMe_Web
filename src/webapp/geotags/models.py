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
    
    def desc_count(self, value=1):
        def _tx(value):
            value = int(value)
            obj = Tag.get(self.key())
            if obj.count > 0:
                obj.count -= value
                obj.put()
        db.run_in_transaction(_tx, value)
            
    def inc_count(self, value=1):
        def _tx(value):
            value = int(value)
            obj = Tag.get(self.key())
            obj.count += value
            obj.put()
        db.run_in_transaction(_tx, value)
        
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
    
    @property
    def _tags(self):
        """Lee la lista de tags y devuelve las instancias"""
        if self.__tags is None:
            self.__tags = Tag.get(self._tags_list)
        return self.__tags
    
    @property
    def tags(self):
        return [tag.name for tag in self._tags]
        
    def _tags_setter(self, tags):
        from types import UnicodeType, StringType, ListType
        """Crea la lista o añade el tag"""
        if type(tags) is StringType:
            tags = unicode(tags)
        if type(tags) is UnicodeType:
            tags = tags.split(SEPARATOR)
        if type(tags) is ListType:
            tags = [t.strip().lower() for t in tags]
            loaded_tags = db.get_async(self._tags_list)  # carga todos los tags existentes en una lista
            for tagInstance in loaded_tags.get_result():
                if tagInstance.name not in tags:  #  un tag ya no esta en la lista nueva, lo borramos
                    self._tags_list.remove(tagInstance.key())
                    tagInstance.desc_count()
            for tag in tags:  # recorremos toda la lista de tags y añadirmos los que sean nuevos
                tagInstance = Tag.get_or_insert(name=tag)
                if tagInstance is not None and not tagInstance.key() in self._tags_list:
                    self._tags_list.append(tagInstance.key())
                    tagInstance.inc_count()
            self.put()
        else:
            raise AttributeError

#    def _remove_tag(self, name):
#        tagInstance = Tag.objects.get_by_name(name)
#        if tagInstance is None:
#            return False
#        self.__tags_list.remove(tagInstance.key())
#        tagInstance.desc_count()
#        return True
#        
#    def _add_tag(self, name):
#        tagInstance = Tag.get_or_insert(name=name)
#        if tagInstance is None:
#            return False
#        self.__tags_list.append(tagInstance.key())
#        tagInstance.inc_count()
#        return True
