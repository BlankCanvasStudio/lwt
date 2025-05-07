#!/bin/bash

DEV=''
CMD=''
FILENAME='pid.tmp'


while [[ $# -gt 0 ]]; do
     case $1 in
         -d) 
            shift
            DEV="$1"
            shift
            ;;
         -n)
            shift
            FILENAME="$1"
            shift
            ;;
         -c)
            shift
            CMD="$1"
            shift
            ;;
         *) 
            echo "Unexpected argument in nfra/exe-with-pid. Quitting"
            exit
    esac
done

ssh $DEV "$CMD > /dev/null 2>&1 & echo PID: \$!" | tail -n 1 | grep "PID" | awk '{print $2}'

# cat $FILENAME 

rm $FILENAME > /dev/null 2> /dev/null

