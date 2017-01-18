#!/bin/bash
set PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
l=`/usr/sbin/exim -bpc`;
n=`hostname`;
echo "exim,host=$n queue=$l";
