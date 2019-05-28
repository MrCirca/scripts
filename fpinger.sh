#/bin/bash

FPING_TARGET=$2
FPING_COUNT=$3
FPING_PERIOD=$4
FPING_BYTES_SIZE=$5
FPING_TIMEOUT=$6
FPING_SRC=$7
USER_PARAM=$8

ZABBIX_SENDER_COMMAND="zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i - >/dev/null | at now &>/dev/null"

FPING_COMMAND="fping -q -c $FPING_COUNT -p $FPING_PERIOD -b $FPING_BYTES_SIZE -t $FPING_TIMEOUT -S $FPING_SRC $FPING_TARGET"

if [ $8 == "agent_ping" ]; then
    echo $($FPING_COMMAND 2> /dev/null && echo 1 || echo 0) | sed -r "s/.*/- agentping_trap[$1] \0/g"

elif [ $8 == "packet_loss" ]; then
    echo $($FPING_COMMAND 2>&1 | egrep -o "([0-9]+\.)?[0-9]+%" | tr -d "%" | sed -r "s/.*/- agentpingloss_trap[$1] \0/g")

elif [ $8 == "sec" ]; then
    echo $($FPING_COMMAND 2>&1 | (egrep -o "(([0-9]+\.)?[0-9]+/?)+$" || echo "0") | ( [[ "$9" == "min" ]] && cut -d "/" -f 1 || [[ "$9" == "avg" ]] && cut -d "/" -f 2 || [[ "$9" == "max" ]] && cut -d "/" -f 3) | sed -r "s/.*/- agentpingsec_trap[min] \0/g")
fi
