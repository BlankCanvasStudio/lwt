#!/bin/bash

source ./config-test.sh

# Shut down the router
echo "Shutting down Click Router"
router_pid=$(ssh $click_collector "pgrep -o click")
ssh $click_collector "sudo kill $router_pid"

