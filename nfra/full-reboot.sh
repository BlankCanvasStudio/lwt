#!/bin/bash
source ./config-test.sh

ssh $filled_router "sudo reboot"
ssh $pipe_gen "sudo reboot"
ssh $pipe_rcv "sudo reboot"
ssh $user_tap "sudo reboot"
ssh $srvr_tap "sudo reboot"
ssh $limiting_router "sudo reboot"
ssh $click_collector "sudo reboot"

ping $click_collector
