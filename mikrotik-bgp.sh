#!/bin/bash
ROUTER_IP=$2
COMMAND="/routing bgp peer print status"
NAME=$(ssh zabbix'@'$ROUTER_IP "$COMMAND" | tail -2 | awk '{print $2}' )
if [ $NAME == "state=established" ]
then
	echo 1
else
	echo 0
fi
