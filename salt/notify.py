#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  DESCRIPTION: check salt stack cpnfig not the same on node
#       AUTHOR: artemirk@gmail.com ()
# ===============================================================================
import subprocess

cmdlist =  open('/srv/file.notify', 'r')
for line in cmdlist:
    cmd,e = subprocess.Popen(line, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    for l in cmd.decode('utf-8').replace(':\n',' ').splitlines():
       srv,state=l.split()
       if state == 'False':
	       print(srv)
