#!/bin/bash

#Path to google app engine server
SERV=/home/hhkaos/Apps/google_appengine/dev_appserver.py
#Path to git repository
REPO=/home/hhkaos/workspace/GeoRemindMe_Web

$SERV \
	--datastore_path=$REPO/src/webapp/fixtures/dev_appserver.datastore \
	$REPO/src/webapp/

read
