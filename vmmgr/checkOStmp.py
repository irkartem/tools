#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json


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
output = subprocess.run("ansible vznode -i /opt/ansible/inventory.py -m shell -a '/opt/listOStmp.py'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
fout = ""
for l in str(output.stdout).split('\n'):
    if 'SUCCESS' in l: continue
    if 'FAIL' in l:
        name = l.split(' ')[0]
        print("can't login {}\n".format(name))
    name,osname,ver = l.strip().split(' ')[:3]
    if (osname not in vzdct.keys()):
        print ("New TMPL {} {} {}\n".format(name,osname,ver))
    if (osname in vzdct.keys()) and (vzdct[osname] != ver):
        print ("wrong TMPL {} {} {}={}\n".format(name,osname,ver,vzdct[osname]))
