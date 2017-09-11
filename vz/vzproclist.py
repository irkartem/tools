#!/usr/bin/python
# parse /proc/$i/stat for procs

import os
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

bad = ['miner']
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
        if (int(k[ctime]) > 100000 or int(k[io]) > 10000) and k[cmd] not in good:
          print '{6} {0} {1} {2} vz={3} cputime={4} io={5}'.format(k[pid],k[cmd],k[state],k[veid],k[ctime],k[io],ip)
  except Exception:
    continue
#need to parse CMD string 
