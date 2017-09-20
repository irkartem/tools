#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re
import sqlite3


DB_STRING = "/opt/ansible/artem/tools/vz/tickets.sqlite"

def killsend(s):
    json_string = {}
    json_string['string_kill'] = s
    r = requests.post('http://mon.ispbug.ru:35000/killproc/api/', data=json.dumps(json_string), headers = {'Content-type': 'application/json', 'Authorization': 'Token dd798c14e26b32c517ca2dd40c372dd4f027ba50'})
    return True

def sshkill(host,pid):
     stdout, stderr = Popen(['ssh', '-q','-o UserKnownHostsFile=/dev/null ','-o StrictHostKeyChecking=no','-o ConnectTimeout=10', 'root@{}'.format(host), 'kill -9 {}'.format(pid)],stdout=PIPE,universal_newlines=True).communicate()
     return stdout


def tocuchticket(tpe,ip,ticket):
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
    white = ['(mysqld)','(monclient)','(postgres)','(nginx)','(ruby)','(node)','(auditd)','(python)','(python2)','(uwsgi)','(php5-fpm)','(gunicorn)','(php)','(terminal.exe)','(mongod)']
    miner = ['(monacoCoind)','(geysercoind)','(minerd)','(coind)','(arcticcoind)','(multichaind)','(cryptonight)']
    kill = ['(core)','(isptar)','(licctl)','(usagestat)']
    output = subprocess.run("/usr/local/bin/ansible vznode -i /opt/ansible/inventory.py -m shell -a '/opt/vzProcs.py'", shell=True, stdout=subprocess.PIPE,universal_newlines=True) 
    #print("/usr/bin/ansible {} -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vemgr vmhostnode'".format(master))
    for l in str(output.stdout).split('\n'):
  :      try:
          host,ip,pid,cmd,state,vid,cpu,io,fcmd = l.split(' ')
        except Exception:
            continue
        try:
            cpu = int(cpu.split('=')[1])
        except Exception:
            cpu = 0
        try:
            io = int(io.split('=')[1])
        except Exception:
            io = 0
        if cpu > 300000 or io > 300000:
            if cmd not in white:
                f.write(" {} {}, {}, {}, {}, {}, cpu {} \n".format(cmd,pid,state,vid,host,ip,cpu,fcmd))
        if cpu > 100000 and 'bash' in cmd:
          killsend("CPU bash with pid {}, {}, veid {}, {}, {}, cpu {}".format(pid,fcmd,vid,host,ip,cpu))
          sshkill(host,pid)
        if cpu > 300000 and cmd in kill:
          #print("######KilledFucking core {} {}, {}, {}, {}, {}, cpu {}".format(pid,state,cmd,vid,host,ip,cpu))
          killsend("CPU core with pid {}, {}, veid {}, {}, {}, cpu {}".format(pid,fcmd,vid,host,ip,cpu))
          sshkill(host,pid)
        if (cpu > 10000 and cmd in miner) or re.match('\(php......_.*',cmd):
          tt = getticket('mine',ip)
          if tt != False:
              print("Need to append ticket {} {}i {}".format(tt,ip,cmd))
              sshkill(host,pid)
          else:
              name = u'Майнинг на VDS {} {}'.format(cmd,ip)
              text = u'''
Здравствуйте, %name%.

Мы заметили, что на вашем сервере %itemname% установлено запрещенное правилами предоставления услуг ПО.
Согласно правилам размещения любой майнинг запрещен во всех видах.

Прямо сейчас я остановил ваш процесс {} {} {}. 

Если это запускали не вы, то вам следует провести расследоваение. Так как ваш сервер взломан. 

При повторении ситуации мы будем вынуждены отказать вам в предоставлении услуг. 
'''.format(pid,state,cmd)
              r = requests.get('https://my.ispsystem.com/mancgi/ticket2client?ip={}&agree=1&{}'.format(ip,urllib.parse.urlencode({'subject': name.encode('utf8'),'message': text.encode('utf8')})))
              out = r.content.decode('utf-8')
              #print("######KilledFucking {} {}, {}, {}, {}, {}, cpu {}".format(pid,state,cmd,vid,host,ip,cpu))
              killsend("Miner have found pid {}, {}, veid {}, {}, {}, ticket {}".format(pid,cmd,vid,host,ip,out))
              sshkill(host,pid)


