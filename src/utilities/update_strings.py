#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
BASE_DIR = path.normpath(path.dirname(__file__))

LANGUAGES = (
  #~ ('ca', u'Català'),
  ('de', u'Deutsch'),
  ('en', u'English'),
  ('es', u'Español'),
  ('fr', u'Francais'),
  #~ ('gl', u'Galego'),
  ('it', u'Italiano'),
  #~ ('nl', u'Nederlands'),
  #~ ('pl', u'Polski'),
  #~ ('zh', u'Chinese'),
  
)

import commands

for lang in LANGUAGES:
	print 'django-admin.py --settings=../webapp makemessages -l '+lang[0]
	if commands.getstatusoutput('django-admin --settings=../webapp makemessages -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	elif commands.getstatusoutput('django-admin.py --settings=../webapp makemessages -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	else:
		print lang[1] + ' strings couldn\'t be updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
		
print 'Now look if there is any translation tagged with #fuzzy or without been translated'
		
