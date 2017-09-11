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


hh = socket.gethostname()
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

bad = ['ArchiSteamFarm','mod-tmp','game','cryptonight','minerd','inergate','arcticcoind','multichaind']
bad = ['core','mgrctl','filemgr']
good = ['(mysqld)','(mongod)']
pid = 0
cmd = 1
state = 2
io = 41
veid = -1
ctime = 13
plist = []
pd = []
for f in pids:
  try:
    with open('/proc/{0}/stat'.format(f), 'r') as ff:
      for l in ff:
        k = l.strip().split(' ')
        try:
          pd.append(int(k[pid]))
          pd.append(k[cmd])
          pd.append(k[state])
          pd.append(int(k[veid]))
          pd.append(int(k[ctime]))
          pd.append(int(k[io]))
          plist.append(pd)
        except Exception:
          continue
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
          print '{7} {6} {0} {1} {2} vz={3} cputime={4} io={5}'.format(k[pid],k[cmd],k[state],k[veid],k[ctime],k[io],ip,hh)
          for bb in kill:
            if bb in k[cmd]:
              killsend(k[pid],'{0} {1} {2} {3} {4}'.format(hh,ip,k[pid],k[cmd],k[veid]))
  except Exception:
    continue
#need to parse CMD string 
