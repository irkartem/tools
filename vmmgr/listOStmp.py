#!/usr/bin/python
# show information about os nodes os templates

import os
import socket

hh = socket.gethostname()
if os.path.isdir("/vm/nfsshare/"):
    for dirname in os.listdir('/vm/nfsshare/'):
        if dirname == 'iso': continue
        pth = "/vm/nfsshare/{0}".format(dirname)
        if os.path.isdir(pth):
            try:
                f = open("{0}/metainfo.xml",'r')
            except Exception:
                print("{0} {1} broken".format(hh,dirname))
                continue
        for line in f.readlines():
            if line.startswith('  <osname>'):
                os = line.split('>')[1].split('<')[0]
            if line.startswith('  <version>'):
                ver = line.split('>')[1].split('<')[0]
        print("{0} {1} {2}".format(hh,os,ver))
if os.path.isdir("/vz/template/cache/"):
    for dirname in os.listdir('/vz/template/cache/'):
        print("{0} {1} {2}".format(hh,dirname,'0'))
