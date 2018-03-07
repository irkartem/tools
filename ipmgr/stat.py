#!/usr/bin/python3.4

import pymysql
import json
import sys
import requests
import ipcalc

def query(q):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='ipmgr',charset='utf8')
    cur = conn.cursor()
    cur.execute("set names utf8")
    cur.execute(q)
    ray = cur.fetchall()
    cur.close()
    conn.close()
    return ray


def getPermbyUserId(id):
    ray=query("select iprange from perm where mgruser={} and iptype=5 and iprange not like '2a01%';".format(id))
    return [x[0] for x in ray]

def getAllIpList():
    ray=query("select i.name,i.mgruser,i.status,i.domain,(select name from dnsbl where id=id.dnsbl) from ip i left join ip2dnsbl id on i.id=id.ip where i.name not like '2a01%';")
    dct={}
    for r in ray:
        t={}
        t['mgruser'] = r[1]
        t['status'] = r[2]
        t['domain'] = r[3]
        t['blockname'] = r[4]
        t['bill'] = 0
        dct[r[0]]=t
    return dct

def getBilledList():
  r = requests.get('https://my.firstvds.ru/mancgi/iplist?auth=cacaFixPanel')
  s = str(r.text)
  out = s.strip().split('\n')
  return out

mgruser={}
for id,name,note in query("SELECT id,name,note FROM mgruser where level=16 and note like '%Prod%'"):
    tt={}
    tt['id']=id
    tt['note']=note
    tt['perm']=getPermbyUserId(id) 
    tt['bill']=0
    tt['used']=0
    tt['block']={}
    tt['free']=0
    tt['pool']=0
    tt['inuse']=[]
    mgruser[name]=tt

#get ip list from ipmgr and bill 
ips = getAllIpList()
for ip in getBilledList():
    if ip.startswith('82.202.168') or ip.startswith('82.202.167'): # airnode skip
        continue
    if ip in ips:
        ips[ip]['bill']=1
    else:
        ...
        #print("Billed but not in list {}".format(ip))
#iterate user and calculate numbers 
for k in mgruser.keys():
    #print("{} {}\n".format(k,mgruser[k]['note']))
    for net in mgruser[k]['perm']:
        for x in ipcalc.Network("{}".format(net)):
            x=str(x)
            if x not in ips:
                print("Ip not in base {}".format(x))
                continue
            mgruser[k]['bill'] += ips[x]['bill']
            if ips[x]['status']==1:
                mgruser[k]['free'] += 1
            elif ips[x]['status']==2:
                mgruser[k]['used'] += 1
                if ips[x]['domain'].startswith('vds.pool'):
                    mgruser[k]['pool'] += 1
            elif ips[x]['status']==5:
                if ips[x]['blockname'] in mgruser[k]['block']:
                    mgruser[k]['block'][ips[x]['blockname']].append(x)
                else:
                    mgruser[k]['block'][ips[x]['blockname']] = [x]
            elif ips[x]['status']==6:
                mgruser[k]['inuse'].append(x)
#    print(mgruser[k])
#print(mgruser)
print(json.dumps(mgruser))


