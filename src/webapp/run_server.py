#!/bin/bash

#Path to google app engine server
SERV=~/Apps/google_appengine/dev_appserver.py
#Path to git repository
REPO=~/workspace/GeoRemindMe_Web

python2.5 $SERV --datastore_path=$REPO/src/fixtures/dev_appserver.datastore $REPO/src/webapp/

read
