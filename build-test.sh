#!/bin/bash

source ./config-test.sh


# Build the click router
echo "Building click router"
./init/xdc/fc.sh $click_collector
./init/xdc/dpdk.sh $click_collector
# Move the click router (Data recorder object is moved when 
#       fastclick is installed so no need to do it here)
scp $router_file $click_collector:"~/router.cpp"


# Make sure the gen files are executable
echo "Making all gen files executable"
chmod +x $pipe_gen_exe
chmod +x $pipe_rcv_exe
chmod +x $tap_gen_exe
chmod +x $tap_rcv_exe

# Move gen files over to user_tap and pipe_gen
echo "Moving files into pipe gen & rcv"
scp $pipe_rcv_exe $pipe_rcv:"~/rcv"
scp $pipe_gen_exe $pipe_gen:"~/gen"

# Move rcv files ove to srvr_tap and pipe_rcv
echo "Moving files into tap gen & rcv"
scp $tap_gen_exe $user_tap:"~/gen"
scp $tap_rcv_exe $srvr_tap:"~/rcv"


# Bind script is moved when dpdk is set up so no need to do it here
# tcpdump is auto installed on every machine. No need to do that here

