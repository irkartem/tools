#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re
import sqlite3


DB_STRING = "/opt/db/isitOk.sqlite"

def read_authfile(path):
    with open(path, 'r') as f:
        return f.read().strip()


def changesend(s):
    json_string = {}
    json_string['mem_info'] = s
    r = requests.post('http://mon.ispbug.ru:35000/killproc/mem/api/', data=json.dumps(json_string), headers = {'Content-type': 'application/json', 'Authorization': 'Token {}'.format(read_authfile('/opt/ansible/artem/tools/vmmgr/auth'))})
    return True

def getMasterNode(host):
     master = host.split('-')[0]
     if master == 'msk':
         master = "{}-{}".format(host.split('-')[0],host.split('-')[1])
     if master == 'wkvm':  master = 'kvm'
     return master
def decreaseLimit(host,elid,lmt):
     master = getMasterNode(host)
     stdout, stderr = Popen(['ssh', '-q','-o UserKnownHostsFile=/dev/null ','-o StrictHostKeyChecking=no','-o ConnectTimeout=10', 'root@{}'.format(master), '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode.edit  elid={} maxvmcount={} sok=ok'.format(elid,lmt)],stdout=PIPE,universal_newlines=True).communicate()
     return stdout

def touchtCount(host,count):
    with sqlite3.connect(DB_STRING) as c:
        r = c.execute("INSERT INTO countlog(name,cluster,count) VALUES (?,?,?)",['meminfo80pcnt',host,count])
    return r


if __name__ == '__main__':
    output = subprocess.run("ansible kvmaster -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode'  | egrep 'meminfo=[8-9][0-9]'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
    pctCount = {}
    fout = ""
    for l in str(output.stdout).split('\n'):
        vls = {}
        for vv in l.strip().split(' '):
            try:
                n,v = vv.split('=')[:2]
                vls[n] = v
            except Exception:
                continue
        if 'name' in vls.keys():
            fout += "name:{} vms:{} limit:{} mem:{}\n".format(vls['name'],vls['countvm'],vls['maxvmcount'],vls['meminfo'])
            master = getMasterNode(vls['name'])
            if master not in pctCount.keys():
                pctCount[master] = 0
            else:
                pctCount[master] += 1
            if vls['name'].startswith('jupiter'):
                continue
            if int(vls['maxvmcount']) < int(vls['countvm']):
                continue
            nlimit = int(vls['countvm']) - 1
            out = decreaseLimit(vls['name'],vls['id'],nlimit)
            print("{} vms:{} limit/old:{}/{} mem:{} output:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo'],out))
            changesend("{} vms:{} limit/old:{}/{} mem:{} output:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo'],out))
    for k in pctCount.keys():
        touchtCount(k,pctCount[k])
    f = open('/var/tmp/artemcheck/node80pctKVM', 'w')
    f.write(fout)
    f.close()
