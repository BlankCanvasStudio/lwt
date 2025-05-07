#!/bin/bash

SERVER="routertwo"
DEV="ens1f2"
BPS="100000000bit"
BURST="1500B"
LATENCY="1us"
DELETE="false"
LIMIT="1500KB"

while [[ $# -gt 0 ]]; do
  case $1 in
      --server) # where to kill
          shift
          SERVER="$1"
          shift
          ;;
      --dev) # what to kill
          shift
          DEV="$1"
          shift
          ;;
      --bps)
          shift
          BPS="$1"
          shift
          ;;
      --burst)
          shift
          BURST="$1"
          shift
          ;;
      --latency)
          shift
          LATENCY="$1"
          shift
          ;;
      --delete)
          DELETE="true"
          shift
          ;;
      *)
              echo "Unexpected argument in nfra/run/limit. Quitting"
              exit
  esac
done

if [ "$DELETE" = "true" ]; then
    ssh $SERVER "sudo tc qdisc del dev $DEV root"
    exit
fi

ssh $SERVER "sudo tc qdisc add dev $DEV root tbf rate $BPS burst $BURST limit $LIMIT" # latency $LATENCY"

