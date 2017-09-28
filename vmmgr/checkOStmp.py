#!/usr/bin/python
# show information about os nodes os templates
import os

vzdct = {}
kvdict = {}
with open('/opt/db/vztempl', 'r') as vzconf:
    for line in vzconf:
        k,v = line.strip().split(' ')[:2]
        vzdict[k] = v

with open('/opt/db/kvtempl', 'r') as vzconf:
    for line in vzconf:
        k,v = line.strip().split(' ')[:2]
        vzdict[k] = v
