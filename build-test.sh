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
if [ "$pipe_uses_iperf3" = true ]; then
    if [ "$pipe_iperf3_udp" = true ]; then
        ./init/xdc/iperf3.sh -c $pipe_gen -s $pipe_rcv -p 12345 \
            -i $pipe_iperf3_interval -ip $pipe_iperf3_server_ip \
            -b $pipe_iperf3_bps -t $test_time -u
    else
        ./init/xdc/iperf3.sh -c $pipe_gen -s $pipe_rcv -p 12345 \
            -i $pipe_iperf3_interval -ip $pipe_iperf3_server_ip \
            -b $pipe_iperf3_bps -t $test_time
    fi
else
    scp $pipe_gen_exe $pipe_gen:"~/gen"
    scp $pipe_rcv_exe $pipe_rcv:"~/rcv"
fi

# Move rcv files ove to srvr_tap and pipe_rcv
echo "Moving files into tap gen & rcv"
if [ "$tap_uses_iperf3" = true ]; then
    if [ "$tap_iperf3_udp" = true ]; then
        ./init/xdc/iperf3.sh -c $user_tap -s $srvr_tap -p 12345 \
            -i $tap_iperf3_interval -ip $tap_iperf3_server_ip \
            -b $tap_iperf3_bps -t $test_time -u
    else
        ./init/xdc/iperf3.sh -c $user_tap -s $srvr_tap -p 12345 \
            -i $tap_iperf3_interval -ip $tap_iperf3_server_ip \
            -b $tap_iperf3_bps -t $test_time
    fi
else
    scp $tap_gen_exe $user_tap:"~/gen"
    scp $tap_rcv_exe $srvr_tap:"~/rcv"
fi

# Bind script is moved when dpdk is set up so no need to do it here
# tcpdump is auto installed on every machine. No need to do that here

