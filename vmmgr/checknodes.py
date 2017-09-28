#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re



if __name__ == '__main__':
    output = subprocess.run("ansible kvmaster -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode'  | egrep 'meminfo=[8-9][0-9]'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
    pctCount = {}
    f = open('/var/tmp/node80pctKVM', 'w')
    for l in str(output.stdout).split('\n'):
        vls = {}
        for vv in l.strip().split(' '):
            try:
                n,v = vv.split('=')[:2]
                vls[n] = v
            except Exception:
                continue
        if 'name' in vls.keys():
            master = getMasterNode(vls['name'])
            if master not in pctCount.keys():
                pctCount[master] = 0
            else:
                pctCount[master] += 1
            f.write("name:{} vms:{} limit:{} mem:{}\n".format(vls['name'],vls['countvm'],vls['maxvmcount'],vls['meminfo']))
            if vls['name'].startswith('jupiter'):
                continue
            #changesend("{} vms:{} limit:{} mem:{}".format(vls['name'],vls['countvm'],vls['maxvmcount'],vls['meminfo']))
            if int(vls['maxvmcount']) < int(vls['countvm']):
                continue
            nlimit = int(vls['countvm']) - 1
            out = decreaseLimit(vls['name'],vls['id'],nlimit)
            print("{} vms:{} limit/old:{}/{} mem:{} output:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo'],out))
            changesend("{} vms:{} limit/old:{}/{} mem:{} output:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo'],out))
    for k in pctCount.keys():
        touchtCount(k,pctCount[k])
