#!/bin/bash
echo $@ > /tmp/send
cat /tmp/send |/bin/mail -E -s "$1 Bad Admin" artem@ispserver.com 
