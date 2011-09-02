#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
BASE_DIR = path.normpath(path.dirname(__file__))

import commands


if commands.getstatusoutput('django-admin compilemessages')[0]==0:#creates german (de) .po
	print ' All strings have been succesfully compiled at \'locale/*/LC_MESSAGES/django.po\''
elif commands.getstatusoutput('django-admin.py compilemessages')[0]==0:#creates german (de) .po
	print ' All strings have been succesfully compiled at \'locale/*/LC_MESSAGES/django.po\''
else:
	print ' Error: the strings could not been succesfully compiled'
	
