#!/usr/bin/python

"""
    To find in work directory and subdirectories: find . -name "*.html"|xargs -L 1 ./bad_trans.py
"""

import re,sys

for line in open(sys.argv[1]).readlines():
    rg = re.search(r'{%\s*trans(?P<str>[^%]+)%}',line)
    if rg:
        if rg.group('str').count("'") %2 or rg.group('str').count('"') %2:
            print(line)
            print(sys.argv[1])
            break
    
