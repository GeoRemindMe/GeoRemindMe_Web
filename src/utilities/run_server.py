#!/bin/bash

#Path to google app engine server
SERV=~/Apps/google_appengine/dev_appserver.py
#Path to git repository
REPO=~/workspace/GeoRemindMe_Web

#Me falla si no tengo la 2.5 instalada
python2.5 $SERV --datastore_path=$REPO/src/fixtures/dev_appserver.datastore $REPO/src/webapp/
#python2.6 ~/Apps/google_appengine/dev_appserver.py --datastore_path=/home/hhkaos/workspace/GeoRemindMe_Web/src/fixtures/dev_appserver.datastore ~/workspace/GeoRemindMe_Web/src/webapp/

read

#!/usr/bin/env python
#~ import commands
#~ import sys
#~ import os
#~ from os import path
#~ 
#~ BASE_DIR = path.normpath(path.dirname(__file__))
#~ HOME_DIR = path.normpath(os.path.expanduser('~'))
#~ 
#~ 
#~ #Path to google app engine server
#~ SERV="/Apps/google_appengine/dev_appserver.py"
#~ #Path to git repository
#~ REPO="/workspace/GeoRemindMe_Web"
#~ 
#~ if sys.version_info[0] < 2 and sys.version_info[1] < 4:
    #~ raise "must use python 2.5 or greater"
#~ else:
	#~ try:
		#~ 'python2.5 $HOME_DIR$SERV --datastore_path=$HOME_DIR$REPO/src/fixtures/dev_appserver.datastore $HOME_DIR$REPO/src/webapp/'
	#~ except:
		#~ eval("python $HOME_DIR$SERV --datastore_path=$HOME_DIR$REPO/src/fixtures/dev_appserver.datastore $HOME_DIR$REPO/src/webapp/")
#~ 
#~ 
#~ 
