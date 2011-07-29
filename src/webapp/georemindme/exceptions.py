# coding:utf-8

"""
.. module:: exceptions
    :platform: appengine
    :synopsis: Excepciones comunes para todo el proyecto
"""


class PrivateException(Exception):
    value = "This instance is private"