#!/usr/bin/python
# parse /proc/$i/stat for procs

import os
import socket


def gettotal():
    with open('/proc/stat') as f:
        ttl = f.readline().strip().split()
        sm = int(ttl[1])+ int(ttl[2]) + int(ttl[3]) + int(ttl[4])
    return sm


hh = socket.gethostname()
pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

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
        with open('/proc/{0}/cmdline'.format(f), 'r') as ff:
          fcmd = ff.read().strip().replace(' ','__')

        print '{7} {6} {0} {1} {2} vz={3} cputime={4} io={5} {8}'.format(k[pid],k[cmd],k[state],k[veid],k[ctime],k[io],ip,hh,fcmd)
  except Exception:
    continue
#need to parse CMD string 
