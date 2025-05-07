#!/bin/bash

echo "Writing /etc/resolv.conf"
ssh $1 "sudo rm /etc/resolv.conf"
ssh $1 "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
ssh $1 "echo 'search system.marstb harbor.system.marstb finalmetal.init.lwt' | sudo tee -a /etc/resolv.conf"
# ssh $1 "echo 'search fake.init.lwt' | sudo tee -a /etc/resolv.conf"

