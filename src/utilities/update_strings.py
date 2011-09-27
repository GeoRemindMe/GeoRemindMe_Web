#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
BASE_DIR = path.normpath(path.dirname(__file__))

LANGUAGES = (
  ('ca', u'Català'),
  #('de', 'Deutsch'),
  ('en', 'English'),
  ('es', u'Español'),
)

import commands

for lang in LANGUAGES:
	if commands.getstatusoutput('django-admin makemessages -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	elif commands.getstatusoutput('django-admin.py makemessages -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	else:
		print lang[1] + ' strings couldn\'t be updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
		
print 'Now look if there is any translation tagged with #fuzzy or without been translated'
		
