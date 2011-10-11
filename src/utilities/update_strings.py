#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
BASE_DIR = path.normpath(path.dirname(__file__))
import commands,os,sys

os.chdir( "../webapp" )
CWD = os.getcwd()
sys.path.append("../webapp")

import settings




print "-> Compilando ficheros de idiomas..."

for lang in settings.LANGUAGES:
	
	if commands.getstatusoutput('django-admin makemessages -v 2 -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	elif commands.getstatusoutput('django-admin.py makemessages -v 2 -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	else:
		print lang[1] + ' strings couldn\'t be updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''

	if commands.getstatusoutput('django-admin makemessages -v 2 -d djangojs -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	elif commands.getstatusoutput('django-admin.py makemessages -v 2 -d djangojs -l '+lang[0])[0]==0:#creates german (de) .po
		print lang[1] + ' strings updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
	else:
		print lang[1] + ' strings couldn\'t be updated at \'locale/'+lang[0]+'/LC_MESSAGES/django.po\''
		
print 'Now look if there is any translation tagged with #fuzzy or without been translated'
		
