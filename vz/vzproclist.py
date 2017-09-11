#!/usr/bin/python
# parse /proc/$i/stat for procs

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
try:
  args = parser.parse_args()
except IOError:
  exit(0)

bad = ['miner']
pid = 0
cmd = 1
state = 2
io = 41
veid = -1
ctime = 13
plist = []
pd = []
for l in args.file.readlines():
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
    exit(0)
  ip='NONE'
  with open('/etc/vz/conf/{0}.conf'.format(k[veid]), 'r') as vzconf:
    for line in vzconf:
      if 'IP_ADDRESS="' in line:
        try:
          ip=line[12:-2].strip().split(' ')[0]
	except Exception:
          ip='NONE'
  if (int(k[ctime]) > 100000 or int(k[io]) > 10000):
    print '{6} {0} {1} {2} vz={3} cputime={4} io={5}'.format(k[pid],k[cmd],k[state],k[veid],k[ctime],k[io],ip)
#need to parse CMD string 
