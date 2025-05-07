#!/bin/bash

proc_names=(
    "gecko"
    "firefox"
    "chrome"
    "Isolated Web Co"
    "gen"
)


for REGEX in ${proc_names[@]}; do

    PIDs=$(ps -e | grep "$REGEX" | awk '{print $1}')

    for pid in $PIDs; do
       sudo kill $pid
    done

done

