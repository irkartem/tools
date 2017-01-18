#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  DESCRIPTION:
#       AUTHOR: artemirk@gmail.com ()
# ===============================================================================
import yaml
import hashlib 
import subprocess

cmdlist =  open('/srv/file.notify', 'r')
for line in cmdlist:
    group,fname = line.strip().split(';')
    with open('/srv/salt/{}'.format(fname), 'r') as stream:
        try:
           dd = yaml.load(stream)
        except yaml.YAMLError as exc:
           print(exc)
        for k, v in dd.items():
            src = [el['source'] for el in  v['file.managed'] if 'source' in el.keys()][0]
            md5 = hashlib.md5(open("/srv/salt/{}".format(src[7:]),'rb').read()).hexdigest()
#            print('salt {} file.check_hash {} md5:{}'.format(group,k,md5))
            cmd,e = subprocess.Popen('salt {} file.check_hash {} md5:{}'.format(group,k,md5), shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
            for l in cmd.decode('utf-8').replace(':\n',' ').splitlines():
               srv,state=l.split()
               if state == 'False':
                  print('File changed {} at server {} \n'.format(k,srv))


