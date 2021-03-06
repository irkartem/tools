#!/usr/bin/python
# show information about os nodes os templates

import os
import socket

hh = socket.gethostname()
osname = ''
ver = ''
dd = ''
if os.path.isdir("/vm/nfsshare/"):
    for dirname in os.listdir('/vm/nfsshare/'):
        if dirname == 'iso': continue
        if dirname == 'recipes': continue
        pth = "/vm/nfsshare/{0}".format(dirname)
        if os.path.isdir(pth):
            try:
                f = open("{0}/metainfo.xml".format(pth),'r')
            except Exception:
                print("{0} {1} broken".format(hh,dirname))
                continue
        for line in f.readlines():
            if '<osname>' in line:
                osname = line.split('>')[1].split('<')[0]
            if '<version>' in line:
                ver = line.split('>')[1].split('<')[0]
            if '<date>' in line:
                dd = line.split('>')[1].split('<')[0].replace(' ','_')
        if osname == '':
            osname = dirname 
        print("{0} {1} {2}:{3}".format(hh,osname,ver,dd))
if os.path.isdir("/vz/template/cache/"):
    for dirname in os.listdir('/vz/template/cache/'):
	sz = os.path.getsize('/vz/template/cache/{0}'.format(dirname))
        print("{0} {1} {2}".format(hh,dirname,sz))
