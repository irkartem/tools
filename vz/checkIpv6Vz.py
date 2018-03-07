#!/usr/bin/python3.6
# collect nodes data
import subprocess
from subprocess import Popen, PIPE
import requests
import json
import urllib.parse
import urllib.request
import sys
from influxdb import InfluxDBClient
from sendstate.send import SenderStateScript

# url = 'https://my.ispsystem.com/mancgi/processingmodule'


def read_authfile(path):
    with open(path, 'r') as f:
        return f.read().strip()


def response(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

def sendinflux(jdata):
    client = InfluxDBClient('store.firstvds.ru', 8086,
                            'cron', 'Yuoph2ah', 'clusters')
    return client.write_points(jdata)

def touchMon(s,st={}):
    ath = read_authfile("/opt/token")
    script = SenderStateScript(token=ath, name_script=s, timeout_fall_hour=8)
    script.send_all_stat(st)


if __name__ == '__main__':
    res = response('http://mon.hoztnode.net/inventory.txt')
    outj = json.loads(res)
    nodes = outj['vznode']
    if len(nodes) < 2:
        sys.exit("Empty list of processingmodules {}".format(nodes))
    tout = 'cron:check IPv66666 \n'
    sendInfo ={}
    for hn in nodes:
        if len(hn) < 3:
            continue
        if 'callisto' in hn:
            continue
        if 'ceres' in hn:
            continue
        output = subprocess.run("/usr/bin/ansible all -f 230  -i '{},' -m shell -a '/bin/ping6 -q -c2 google.com >/dev/null; /bin/echo $?'".format(hn,), shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        out = str(output.stdout).split('\n')
        if out[1] != '0':
            tout += "IPv6 BROKEN {}\n".format(hn)
            sendInfo[hn] = 'broken'
    print(tout)
    if len(tout) > 30:
       r = requests.post('http://mon.ispsystem.net/telegram_senderart.py', data={'text':tout})
       requests.post('http://mon.ispsystem.net/telegram_sender.py', data={'type':'group','text':tout})
       if r.status_code > 250:
           print("can't sent telegram data {} {}".format(r, tout))
    touchMon('Cron_ipv6_broken',sendInfo)
