#!/usr/bin/python
# parse /proc/$i/stat for procs

import os
import socket
import requests


def killsend(pid,s):
    json_string = '{"string_kill": {0}}'.format(s)
    requests.post('http://mon.ispbug.ru:35001/killproc/api/', data=json_string, headers={'Content-Type': 'application/json'})
    #os.kill(pid, 15)
    print "\033[93m ####### Should kill {0} {1} ######### \033[0m".format(s)

def gettotal():
    with open'/proc/stat') as f:
        ttl = f.readline().strip().split()
        sm = int(ttl[1])+ int(ttl[2]) + int(ttl[3]) + int(ttl[4])
    return sm


hh = socket.gethostname()
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

bad = ['ArchiSteamFarm','mod-tmp','game','cryptonight','minerd','inergate','arcticcoind','multichaind']
bad = ['core','mgrctl','filemgr']
good = ['(aggregator)','(apache2)','(atd)','(auditd)','(bash)','(beam.smp)','(bird)','(bundle)','(clamd)','(dbus-daemon)','(dovecot)','(ezstream)','(fail2ban-server)','(freshclam)','(gitlab-mon)','(gunicorn)','(hald)','(httpd)','(icecast2)','(ihttpd)','(init)','(inotifywait)','(java)','(liquidsoap)','(master)','(monit)','(named)','(nginx)','(node_exporter)','(ntpd)','(otrs.Daemon.pl)','(packagekitd)','(php-fpm)','(postgres)','(postgres_export)','(proftpd)','(prometheus)','(python2)','(qmgr)','(radiopoint)','(redis-server)','(rsyslogd)','(salt-minion)','(searchd)','(squid)','(sshd)','(supervisord)','(systemd)','(systemd-journal)','(systemd-logind)','(terminal.exe)','(ts3server)','(tuned)','(/usr/sbin/postg)','(/usr/sbin/spamd)','(uwsgi)']
pid = 0
cmd = 1
state = 2
io = 41
veid = -1
ctime = 13
try:
    t = gettotal()
except Exception:
  total = 1


for f in pids:
  try:
    with open('/proc/{0}/stat'.format(f), 'r') as ff:
      for l in ff:
        k = l.strip().split(' ')
        ip='NONE'
        with open('/etc/vz/conf/{0}.conf'.format(k[veid]), 'r') as vzconf:
          for line in vzconf:
            if 'IP_ADDRESS="' in line:
              try:
                ip=line[12:-2].strip().split(' ')[0]
              except Exception:
                ip='NONE'
        for bb in bad:
          if bb in k[cmd]:
            killsend(k[pid],'{0} {1} {2} {3} {4}'.format(hh,ip,k[pid],k[cmd],k[veid]))
        if (int(k[ctime]) > 100000 or int(k[io]) > 10000) and k[cmd] not in good:
          print '{7} {6} {0} {1} {2} vz={3} cputime={4} io={5}i {8}'.format(k[pid],k[cmd],k[state],k[veid],k[ctime],k[io],ip,hh,t)
          for bb in kill:
            if bb in k[cmd]:
              killsend(k[pid],'{0} {1} {2} {3} {4}'.format(hh,ip,k[pid],k[cmd],k[veid]))
  except Exception:
    continue
#need to parse CMD string 
