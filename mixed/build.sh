#!/bin/bash

# Set default arguments
config_file="./mixed-config.sh"

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

    for (( i=0; i<${#pipe_uses_iperf3_array[@]}; i++ )); do
        if [[ "${pipe_uses_iperf3_array[i]}" == "true" ]]; then
            ssh ${pipe_rcv_array[i]} "sudo rm -rf ~/iperf"
            ssh ${pipe_gen_array[i]} "sudo rm -rf ~/iperf"
        fi
    done

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
for element in "${tap_gen_exe_array[@]}"; do
    chmod +x $element*
done
for element in "${pipe_rcv_exe_array[@]}"; do
    chmod +x $element*
done


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




# Loop for all possible combinations
#
# Move rcv files ove to srvr_tap and pipe_rcv
echo "Moving files into tap gen & rcv"

for (( i=0; i<${#tap_uses_iperf3_array[@]}; i++ )); do

    if [ "${tap_uses_iperf3_array[i]}" = true ]; then
        if [ "${tap_iperf3_udp_array[i]}" = true ]; then
            ./init/xdc/iperf3.sh -c ${user_tap_array[i]} -s ${srvr_tap_array[i]} -p 12345 \
                -i ${tap_iperf3_interval_array[i]} -ip ${tap_iperf3_server_ip_array[i]} \
                -b ${tap_iperf3_bps_array[i]} -t $test_time -u \
                -o ${tap_iperf3_output_file_array[i]} \
                -pt ${tap_iperf3_pacing_array[i]} \
                -P ${tap_iperf3_parallel_array[i]} \
                -fq ${tap_iperf3_fq_rate_array[i]} \
                -x ${tap_iperf3_copies_array[i]} \
                -l ${tap_iperf3_length_array[i]} \
                -n "-tap-$i"

        else
            ./init/xdc/iperf3.sh -c ${user_tap_array[i]} -s ${srvr_tap_array[i]} -p 12345 \
                -i ${tap_iperf3_interval_array[i]} -ip ${tap_iperf3_server_ip_array[i]} \
                -b ${tap_iperf3_bps_array[i]} -t $test_time \
                -o ${tap_iperf3_output_file_array[i]} \
                -pt ${tap_iperf3_pacing_array[i]} \
                -P ${tap_iperf3_parallel_array[i]} \
                -fq ${tap_iperf3_fq_rate_array[i]} \
                -x ${tap_iperf3_copies_array[i]} \
                -l ${tap_iperf3_length_array[i]} \
                -n "-tap-$i"

        fi
    else
        scp ${tap_gen_exe_array[i]} ${user_tap_array[i]}:"~/gen-tap-$i"
        scp ${tap_rcv_exe_array[i]} ${srvr_tap_array[i]}:"~/rcv-tap-$i"

        # Copy things over to the infra
        scp ${tap_gen_build_array[i]} ${user_tap_array[i]}:"~/build-gen-$i.sh"
        scp ${tap_rcv_build_array[i]} ${srvr_tap_array[i]}:"~/build-rcv-$i.sh"
        # Build the infra structure
        ssh ${user_tap_array[i]} "~/build-gen-$i.sh"
        ssh ${srvr_tap_array[i]} "~/build-rcv-$i.sh"
    fi
done


# Copy over the destructors
for (( i=0; i<${#tap_gen_destructor_array[@]}; i++ )); do
    scp ${tap_gen_destructor_array[i]} ${user_tap_array[i]}:"~/gen-destructor-$i"
done
for (( i=0; i<${#tap_rcv_destructor_array[@]}; i++ )); do
    scp ${tap_rcv_destructor_array[i]} ${srvr_tap_array[i]}:"~/rcv-destructor-$i"
done


# Set to circular routing if necessary
if [ "$tap_user_resolve_via_tapsrvr" = "true" ]; then
    ./nfra/update/looped-default-routers.sh setup
fi
if [ "$tap_user_resolve_via_tapuser" = "true" ]; then
    ./nfra/update/looped-default-routers.sh reverse
fi


# Set up clickrcv to be invisible
./nfra/update/clickrcv-routing.sh

