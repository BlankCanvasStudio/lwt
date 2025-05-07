#!/bin/bash

# Set default arguments
config_file="./config-test.sh"

# Parse the commandline arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -c) # config
        shift
        config_file="$1"
        shift
        ;;
    *)
        echo "Unexpected argument in build-test.sh. Quitting"
        exit
    esac
done


source $config_file


./nfra/update/resolve.conf.sh $click_collector
./nfra/update/looped-default-routers.sh takedown # just in case
# Turn off systemd-timesyncd ssh $click_collector "sudo systemctl stop systemd-timesyncd"
# Install policyket-1 so systemd doesn't run into permission error
ssh $click_collector "sudo apt install -y policykit-1"
# Kill the foundry service cause it acts up when you change routing
ssh $click_collector "sudo systemctl stop foundryc"
ssh $click_collector "sudo systemctl stop systemd-timesyncd"
ssh $click_collector "sudo systemctl stop systemd-networkd"


# Build the click router
echo "Building click router"
if [[ "$1" == "-f" ]]; then 
    ./init/xdc/fc.sh -f $click_collector
    if [[ "$tap_uses_iperf3" == "true" ]]; then
        ssh $user_tap "sudo rm -rf ~/iperf"
        ssh $srvr_tap "sudo rm -rf ~/iperf"
    fi
    if [[ "$pipe_uses_iperf3" == "true" ]]; then
        ssh $pipe_rcv "sudo rm -rf ~/iperf"
        ssh $pipe_gen "sudo rm -rf ~/iperf"
    fi
else
    ./init/xdc/fc.sh $click_collector
fi

./init/xdc/dpdk.sh $click_collector
# Move the click router (Data recorder object is moved when 
#       fastclick is installed so no need to do it here)
scp $router_file $click_collector:"~/router.cpp"


# Build the limiting router if applicable
if [ "$run_limiting_router" = "true" ]; then
    ./init/xdc/dpdk.sh $limiting_router
    ./init/xdc/fc.sh $limiting_router
    ./nfra/run/enable-shaping.sh update
fi

# Build the limiting router if applicable
if [ "$run_dpdk_router_two" = "true" ]; then
    ./init/xdc/dpdk.sh $routertwo
    ./init/xdc/fc.sh $routertwo
    ./nfra/run/second-router-limiting.sh update
fi


# Build the click gen limiting
if [ "$run_limiting_router" = "true" ]; then
    ./init/xdc/dpdk.sh clickgen
    ./init/xdc/fc.sh clickgen
    ./nfra/run/click-gen-shaping.sh update
fi


# Make sure the gen files are executable
echo "Making all gen files executable"
chmod +x $pipe_gen_exe*
chmod +x $pipe_rcv_exe*
chmod +x $tap_gen_exe*
chmod +x $tap_rcv_exe*

# Move gen files over to user_tap and pipe_gen
echo "Moving files into pipe gen & rcv"
if [ "$pipe_uses_iperf3" = true ]; then
    pipe_time=$(($tap_start_end_delay + $test_time + $tap_start_end_delay))
    if [ "$pipe_iperf3_udp" = true ]; then
        ./init/xdc/iperf3.sh -c $pipe_gen -s $pipe_rcv -p 12345 \
            -i $pipe_iperf3_interval -ip $pipe_iperf3_server_ip \
            -b $pipe_iperf3_bps -t $pipe_time -u \
            -o $pipe_iperf3_output_file \
            -pt $pipe_iperf3_pacing \
            -P $pipe_iperf3_parallel \
            -fq $pipe_iperf3_fq_rate \
            -x $pipe_iperf3_copies \
       	    -l $pipe_iperf3_length \
            -n "-pipe"

    else
        ./init/xdc/iperf3.sh -c $pipe_gen -s $pipe_rcv -p 12345 \
            -i $pipe_iperf3_interval -ip $pipe_iperf3_server_ip \
            -b $pipe_iperf3_bps -t $pipe_time \
            -o $pipe_iperf3_output_file \
            -pt $pipe_iperf3_pacing \
            -P $pipe_iperf3_parallel \
            -fq $pipe_iperf3_fq_rate \
            -x $pipe_iperf3_copies \
       	    -l $pipe_iperf3_length \
            -n "-pipe"

    fi
else
    scp $pipe_gen_exe $pipe_gen:"~/gen-pipe"
    scp $pipe_rcv_exe $pipe_rcv:"~/rcv-pipe"
fi

# Move rcv files ove to srvr_tap and pipe_rcv
echo "Moving files into tap gen & rcv"
if [ "$tap_uses_iperf3" = true ]; then
    if [ "$tap_iperf3_udp" = true ]; then
        ./init/xdc/iperf3.sh -c $user_tap -s $srvr_tap -p 12345 \
            -i $tap_iperf3_interval -ip $tap_iperf3_server_ip \
            -b $tap_iperf3_bps -t $test_time -u \
            -o $tap_iperf3_output_file \
            -pt $tap_iperf3_pacing \
            -P $tap_iperf3_parallel \
            -fq $tap_iperf3_fq_rate \
            -x $tap_iperf3_copies \
	    -l $tap_iperf3_length \
            -n "-tap"

    else
        ./init/xdc/iperf3.sh -c $user_tap -s $srvr_tap -p 12345 \
            -i $tap_iperf3_interval -ip $tap_iperf3_server_ip \
            -b $tap_iperf3_bps -t $test_time \
            -o $tap_iperf3_output_file \
            -pt $tap_iperf3_pacing \
            -P $tap_iperf3_parallel \
            -fq $tap_iperf3_fq_rate \
            -x $tap_iperf3_copies \
       	    -l $tap_iperf3_length \
            -n "-tap"

    fi
else
    scp $tap_gen_exe $user_tap:"~/gen-tap"
    scp $tap_rcv_exe $srvr_tap:"~/rcv-tap"

    # Copy things over to the infra
    scp $tap_gen_build $user_tap:"~/build-gen.sh"
    scp $tap_rcv_build $srvr_tap:"~/build-rcv.sh"
    # Build the infra structure
    ssh $user_tap "~/build-gen.sh"
    ssh $srvr_tap "~/build-rcv.sh"
fi

# Copy over the destructors
scp $tap_gen_destructor $user_tap:"~/gen-destructor"
scp $tap_rcv_destructor $srvr_tap:"~/rcv-destructor"




# Set to circular routing if necessary
if [ "$tap_user_resolve_via_tapsrvr" = "true" ]; then
    ./nfra/update/looped-default-routers.sh setup
fi
if [ "$tap_user_resolve_via_tapuser" = "true" ]; then
    ./nfra/update/looped-default-routers.sh reverse
fi

# Set up clickrcv to be invisible
./nfra/update/clickrcv-routing.sh


# Bind script is moved when dpdk is set up so no need to do it here
# tcpdump is auto installed on every machine. No need to do that here

# Increase the udp window size
# sudo -S sysctl -w net.ipv4.udp_mem=65536 > ~/tmp-params; sudo -S cp ~/tmp-params /etc/sysctl.conf
