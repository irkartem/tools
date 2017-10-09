#!/usr/bin/python3

import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import re
import sqlite3
import datetime


DB_STRING = "/opt/db/tickets.sqlite"

def killsend(s):
    json_string = {}
    json_string['string_kill'] = s.strip().replace('\x00','')
    r = requests.post('http://mon.ispbug.ru:35000/killproc/api/', data=json.dumps(json_string), headers = {'Content-type': 'application/json', 'Authorization': 'Token dd798c14e26b32c517ca2dd40c372dd4f027ba50'})
    print(r)
    print(json_string)
    if r.status_code != 200:
        f = open('/var/tmp/artemcheck/error-procsforkill', 'a')
        f.write(" {} {}\n".format(datetime.date.today(),s))
        f.close
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
    f = open('/var/tmp/artemcheck/procsforkill', 'w')
    lst = []
    white = ['(mysqld)','(monclient)','(postgres)','(nginx)','(ruby)','(node)','(auditd)','(python)','(python2)','(uwsgi)','(php5-fpm)','(gunicorn)','(php)','(terminal.exe)','(mongod)','(influxd)','(php-fpm)','(qmgr)','(redis-server)','(nagios)','(httpd)','(mysqld_safe)','(httpd.itk)','(uwsgi-core)','(php-fpm7.0)','(apache2)']
    miner = ['(monacoCoind)','(geysercoind)','(minerd)','(coind)','(arcticcoind)','(multichaind)','(cryptonight)','(bitsendd)']
    kill = ['(core)','(licctl)','(usagestat)','(isptar)']
    game = ['(samp03svr)','(hlds_linux)','(hlds_i686)','(srcds_linux)','(ioq3ded)']
    output = subprocess.run("/usr/local/bin/ansible vznode -i /opt/ansible/inventory.py -m shell -a '/opt/vzProcs.py'", shell=True, stdout=subprocess.PIPE,universal_newlines=True)
    #print("/usr/bin/ansible {} -i /opt/ansible/inventory.py -m shell -a '/usr/local/mgr5/sbin/mgrctl -m vemgr vmhostnode'".format(master))
    tout = "mon.hour getBad.py "
    for l in str(output.stdout).split('\n'):
        try:
          host,ip,pid,cmd,state,vid,cpu,io,fcmd = l.split(' ')
          fcmd = fcmd.strip()
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
                f.write(" {} {}, {}, {}, {}, {}, cpu {} {}\n".format(cmd,pid,state,vid,host,ip,cpu,fcmd))
        if cpu > 100000 and 'bash' in cmd:
          killsend("CPU bash with pid {}, {}, veid {}, {}, {}, cpu {}".format(pid,fcmd,vid,host,ip,cpu))
          sshkill(host,pid)
        if cpu > 300000 and cmd in kill:
          #print("######KilledFucking core {} {}, {}, {}, {}, {}, cpu {}".format(pid,state,cmd,vid,host,ip,cpu))
          killsend("CPU core with pid {}, {}, veid {}, {}, {}, cpu {}".format(pid,fcmd,vid,host,ip,cpu))
          sshkill(host,pid)
        if (cpu > 10000 and cmd in miner) or re.match('\(php......_.*',cmd) or re.match('\(minergate-cli.*',cmd):
          tt = getticket('mine',ip)
          if tt != False:
              print("Need to append ticket {} {}i {}".format(tt,ip,cmd))
              sshkill(host,pid)
              tout += "Double detect {} {} {}   {}\n".format('miner',tt.replace('\n', ' ').replace('\r', ''),ip,fcmd)
              killsend("Double detect {} {} {}   {}\n".format('miner',tt.replace('\n', ' ').replace('\r', ''),ip,fcmd))
          else:
              name = u'Майнинг на VDS {} {}'.format(cmd,ip)
              text = u'''
Здравствуйте, %name%.

Мы заметили, что на вашем сервере %itemname% установлено запрещенное правилами предоставления услуг ПО.
Согласно правилам размещения любой майнинг запрещен во всех видах.

Прямо сейчас я остановил ваш процесс {} {} {}.

Вам необходимо принять для предотвращения повторения этой ситуации. И написать в этот тикет какие меры приняты.

В противном случае мы будем вынуждены остановить ваш VDS.

{}
'''.format(pid,state,cmd,fcmd)
              r = requests.get('https://my.ispsystem.com/mancgi/ticket2client?ip={}&agree=1&warn=1&{}'.format(ip,urllib.parse.urlencode({'subject': name.encode('utf8'),'message': text.encode('utf8')})))
              out = r.content.decode('utf-8')
              #print("######KilledFucking {} {}, {}, {}, {}, {}, cpu {}".format(pid,state,cmd,vid,host,ip,cpu))
              touchticket('mine',ip,out)
              killsend("Miner have found pid {}, {}, veid {}, {}, {}, ticket {}".format(pid,fcmd,vid,host,ip,out))
              sshkill(host,pid)
    if tout != "mon.hour getBad.py ":
        killsend(tout)
        #requests.post('http://mon.ispsystem.net/telegram_senderart.py',data={'text':tout})


