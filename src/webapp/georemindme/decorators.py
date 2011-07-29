# coding=utf-8

"""
.. module:: decorators
    :platform: appengine
    :synopsis: Decoradores comunes para todo el proyecto
"""


class classproperty(object):
    '''
    Define una propiedad de clase
    '''
    def __init__(self, getter):
        """getter es la referencia a la funcion de la clase
        que tendra esta propiedad
        """ 
        self._getter = getter

    def __get__(self, instance, owner):
        """owner es la clase donde esta la funcion objects,
        seria el parametro self de objects(self) si estuvieramos llamando
        a la funcion directamente en vez de convertirla en propiedad
        """
        return self._getter(owner)