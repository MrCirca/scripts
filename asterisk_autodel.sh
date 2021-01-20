#!/bin/bash

PATH='/usr/bin:/bin'

ROOT_PATH=/var/spool/asterisk/monitor/
USAGE_THRESHOLD=99

while (( `df -P ${ROOT_PATH} | tail -1 | awk '{print $5}' | sed 's/\%//'` >= ${USAGE_THRESHOLD} ))
do
        rm -rf "`find ${ROOT_PATH}/*/*/* -type d | sort -n -k 2 | head -1`"
done

~                                                                                                                                                                                                                                                             
~                                      
