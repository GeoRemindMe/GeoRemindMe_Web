#!/usr/bin/python
# coding=utf-8

import os,sys

files = {}

BASE_DIR = os.path.abspath(sys.argv[1])

def find(dir):
    
    for f in os.listdir(dir):
        
        if f not in ('.','..',):

            if os.path.isdir(os.path.join(dir,f)):
                find(os.path.join(dir,f))
            else:
                files[f] = files.get(f,[]) + [dir]

find(BASE_DIR)

for f in files.keys():
    if len(files[f])>1:
        print f, [os.path.relpath(d,BASE_DIR) for d in files[f] ]

