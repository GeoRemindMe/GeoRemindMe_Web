#!/bin/bash

#Path to google app engine server
SERV=dev_appserver.py
#Path to git repository
REPO=/Users/valverde/Development/GeoRemindMe_Web

$SERV \
	--datastore_path=$REPO/src/webapp/fixtures/dev_appserver.datastore \
	$REPO/src/webapp/
