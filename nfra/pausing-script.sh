#!/bin/bash

INIT_DELAY=0
RUN_TIME=0
PAUSE_TIME=0

PID_FILE='pid.tmp'

DEV=''
COMMAND=''

pid=''


cleanup() {
    echo "Cleaning up and exiting..."
    # Add cleanup code here, such as stopping any running processes
    exit 0
    ./nfra/kill.sh --server "$DEV" -P $pid
}

trap 'cleanup' SIGTERM SIGINT


while [[ $# -gt 0 ]]; do
     case $1 in
            
         --init-delay)
            shift
            INIT_DELAY="$1"
            shift
            ;;

         --run-time)
            shift
            RUN_TIME="$1"
            shift
            ;;

         --pause-time)
            shift
            PAUSE_TIME="$1"
            shift
            ;;

        --pid-file)
            shift
            PID_FILE="$1"
            shift
            ;;

        --dev)
            shift
            DEV="$1"
            shift
            ;;

        --cmd)
            shift
            COMMAND="$1"
            shift
            ;;

         *) 
            echo "Unexpected argument in nfra/run/build-pausing-script. Quitting"
            exit
    esac
done

sleep $INIT_DELAY

while true; do

    pid=$(./nfra/exe-with-pid.sh -d "$DEV" -c "$COMMAND" -n "$PID_FILE")
    echo "Kill script $$ : $pid"

    sleep $RUN_TIME

    echo "Kill script $$ : Killing $pid"
    ./nfra/kill.sh --server "$DEV" -P $pid

    sleep $PAUSE_TIME

done

