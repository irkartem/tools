#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re
import sqlite3


DB_STRING = "/opt/db/tickets.sqlite"

def read_authfile(path):
    with open(path, 'r') as f:
        return f.read().strip()


def changesend(s):
    json_string = {}
    json_string['mem_info'] = s
    r = requests.post('http://mon.ispbug.ru:35000/killproc/mem/api/', data=json.dumps(json_string), headers = {'Content-type': 'application/json', 'Authorization': 'Token {}'.format(read_authfile('/opt/ansible/artem/tools/vmmgr/auth'))})
    return True

def decreaseLimit(host,elid,lmt):
     master = host.split('-')[0]
     if master == 'msk':
         master = "{}-{}".format(host.split('-')[0],host.split('-')[1])
     if master == 'wkvm':  master = 'kvm'
     stdout, stderr = Popen(['ssh', '-q','-o UserKnownHostsFile=/dev/null ','-o StrictHostKeyChecking=no','-o ConnectTimeout=10', 'root@{}'.format(master), '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode.edit  elid={} maxvmcount={} sok=ok'.format(elid,lmt)],stdout=PIPE,universal_newlines=True).communicate()
     return stdout




if __name__ == '__main__':
    output = subprocess.run("ansible kvmaster -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode'  | egrep 'meminfo=[8-9][0-9]'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
    for l in str(output.stdout).split('\n'):
        vls = {}
        for vv in l.strip().split(' '):
            try:
                n,v = vv.split('=')[:2]
                vls[n] = v
            except Exception:
                continue
        if 'name' in vls.keys():
            if vls['name'].startswith('jupiter'):
                continue
            #changesend("{} vms:{} limit:{} mem:{}".format(vls['name'],vls['countvm'],vls['maxvmcount'],vls['meminfo']))
            if int(vls['maxvmcount']) < int(vls['countvm']):
                continue
            print("{} vms:{} limit/old:{}/{} mem:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo']))
            out = decreaseLimit(vls['name'],vls['id'],nlimit)
            print("{} vms:{} limit/old:{}/{} mem:{} output:{}".format(vls['name'],vls['countvm'],nlimit,vls['maxvmcount'],vls['meminfo'],out))
