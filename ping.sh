#/bin/bash

METRIC=$1
DEST=$2
SOURCE=$3
COUNT=2
PING_COMMAND=$(ping -c "$COUNT" "$DEST" -I "$SOURCE")

if [ "$METRIC" == "packet_loss" ]; then
    PACKET_LOSS_PING=$(echo -e "$PING_COMMAND" | grep "packet loss" | cut -d " " -f 6)
    echo "$PACKET_LOSS_PING"

elif [ "$METRIC" == "latency_min" ]; then
    LATENCY_MIN=$(echo -e "$PING_COMMAND" | grep "rtt" | cut -d "/" -f 4 | cut -d "=" -f 2 | cut -d " " -f 2)
    echo "$LATENCY_MIN"

elif [ "$METRIC" == "latency_avg" ]; then
    LATENCY_AVG=$(echo -e "$PING_COMMAND" | grep "rtt" | cut -d "/" -f 5 | cut -d " " -f 1)
    echo "$LATENCY_AVG"

elif [ "$METRIC" == "latency_max" ]; then
    LATENCY_MAX=$(echo -e "$PING_COMMAND" | grep "rtt" | cut -d "/" -f 6)
    echo "$LATENCY_MAX"

elif [ "$METRIC" == "latency_mdev" ]; then
    LATENCY_MDEV=$(echo -e "$PING_COMMAND" | grep "rtt" | cut -d "/" -f 7)
    echo "$LATENCY_MDEV"

else
   echo "Wrong metric argument"
fi
