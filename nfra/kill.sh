#!/bin/bash

SERVER="localhost"
REGEX="none"
PID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --server) # where to kill
        shift
        SERVER="$1"
        shift
        ;;
    --regex) # what to kill
        shift
        REGEX="$1"
        shift
        ;;
    -P)
        shift
        PID="$1"
        shift
        ;;
    *)
        echo "Unexpected argument in nfra/kill. Quitting"
        exit
esac
done


if [ -z "$PID" ]; then

    get_pid="ps -e | grep \"$REGEX\" | awk '{print \$1}'"
    PIDs=$(ssh $SERVER "$get_pid")

    echo "Killing $PROGRAM on $SERVER"
    for pid in $PIDs; do
        echo "Killing PID: $pid"
        ssh $SERVER "sudo kill $pid"
    done

else

    echo "Killing $PID on $SERVER"
    ssh $SERVER "sudo pkill -P $PID"
    ssh $SERVER "sudo kill $PID"

fi
