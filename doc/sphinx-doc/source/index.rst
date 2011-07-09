.. GeoRoute documentation master file, created by
   sphinx-quickstart on Tue Apr  5 18:16:43 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentación de GeoRemindMe Webapp!
====================================

GeoRemindMe es un proyecto que está estructurado en diferentes paquetes 
que agrupan diferentes funcionalidades dentro de la aplicación.

El funcionamiento general de la aplicación **es simple**, funciona del 
siguiente modo:

Cada URL de la aplicación llama a una función declarada dentro de una 
determinada vista, y esta puede o no llamar a su vez a otras funciones 
de la misma o de las vistas de otros paquetes.

Indices y tablas
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Modelado de la base de datos
===============================
En el siguiente diagrama resume la estructura de la aplicación:

.. image:: ../../database/modelo.jpeg
    :width: 980px
    :align: center
    :alt: Diagrama de la base de datos


Paquetes
===========
Estos paquetes son:

.. toctree::
   	:maxdepth: 2
	
        geouser
        geoauth
        georoute
        geoajax
        geoalert
    
	
.. note::
    
    Dentro de esta aplicación se encuentra la aplicación para Facebook.

