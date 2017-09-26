#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re
import sqlite3


DB_STRING = "/opt/db/tickets.sqlite"

def killsend(s):
    json_string = {}
    json_string['string_kill'] = s
    r = requests.post('http://mon.ispbug.ru:35000/killproc/api/', data=json.dumps(json_string), headers = {'Content-type': 'application/json', 'Authorization': 'Token dd798c14e26b32c517ca2dd40c372dd4f027ba50'})
    return True

def sshkill(host,pid):
     stdout, stderr = Popen(['ssh', '-q','-o UserKnownHostsFile=/dev/null ','-o StrictHostKeyChecking=no','-o ConnectTimeout=10', 'root@{}'.format(host), 'kill -9 {}'.format(pid)],stdout=PIPE,universal_newlines=True).communicate()
     return stdout


def touchticket(tpe,ip,ticket):
    with sqlite3.connect(DB_STRING) as c:
        r = c.execute("INSERT INTO tickets(type,ip,ticket) VALUES (?,?,?)",[tpe,ip,ticket])
    return r

def getticket(tpe,ip):
  with sqlite3.connect(DB_STRING) as c:
       #r = c.execute("SELECT t, data FROM log where t>= datetime('now', '-1 minutes','localtime');")
       r = c.execute("select ticket from tickets where type=? and ip=?;",[tpe,ip])
       ip = r.fetchone()
       if ip:
           return ip[0]
       else:
         return False


if __name__ == '__main__':
    f = open('/var/tmp/procsforkill', 'w')
    lst = []
    output = subprocess.run("ansible kvmaster -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vmmgr vmhostnode'  | egrep 'meminfo=[8-9][0-9]'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
    for l in str(output.stdout).split('\n'):
        print(l)
