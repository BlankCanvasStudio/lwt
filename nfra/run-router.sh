#!/bin/bash

source ./config-test.sh

echo "Writing /etc/resolv.conf"
ssh $click_collector "sudo rm /etc/resolv.conf"
ssh $click_collector "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
ssh $click_collector "echo 'search build.init.lwt' | sudo tee -a /etc/resolv.conf"

# Set up the data collection

echo "Starting click data collector"
# Remove the old data from the click collector
ssh $click_collector "rm -f $loc_click_datafile"
# Make sure the interface is bound
ssh $click_collector "~/bind.sh $tap_interface" # Don't mute in case
ssh $click_collector "~/bind.sh $internet_interface" # Bind the internet interface as well
# Start the click router
if [ "$1" = "-s" ]; then
   ssh $click_collector "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk" &
else
    ssh $click_collector "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk"
fi


