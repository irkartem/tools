#!/bin/bash

### ABOUT
### Runs rsync, retrying on errors up to a maximum number of tries.
### Simply edit the rsync line in the script to whatever parameters you need.

# Trap interrupts and exit instead of continuing the loop
trap "echo Exited!; exit;" SIGINT SIGTERM

MAX_RETRIES=10
i=0

# Set the initial return value to failure
false

while [ $? -ne 0 -a $i -lt $MAX_RETRIES ]
do
     i=$(($i+1))
      /usr/bin/rsync --timeout=6 $@
  done

  if [ $i -eq $MAX_RETRIES ]
  then
        echo "Hit maximum number of retries, giving up."
          exit $?
      fi

