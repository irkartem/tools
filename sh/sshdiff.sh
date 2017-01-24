#!/bin/bash
echo "$1 file $2 changed:" > /tmp/send
/usr/bin/ssh $1 "cat $2" | diff - $3>> /tmp/send 
cat /tmp/send |/bin/mail -E -s "Site changed" artem@ispserver.com 
