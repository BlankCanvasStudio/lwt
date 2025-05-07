#!/bin/bash

# Set default arguments
REPS=1
config_file="./mixed-config.sh"
data_dir_in=""
N_SPECIFIED=false

# Parse the commandline arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -c) # config
        shift
        config_file="$1"
        shift
        ;;
    -n) #number of repetitions
        shift
        REPS="$1"
        N_SPECIFIED=true
        shift
        ;;
    *)
        echo "Unexpected argument in run-test.sh. Quitting"
        exit
    esac
done



# Import the config settings so everything is easy to manage
source $config_file
if [ "$N_SPECIFIED" = "false" ]; then
    REPS=$repititions;
fi


if [ -n "$data_dir_in" ]; then
    data_dir=$data_dir_in
fi


for ((i = 0; i < $REPS; i++)); do
    export expr_name="$expr_name_base-$i"
    echo "name: $expr_name"


    # Verify that the folder doesn't already exist
    export data_path="$data_dir/$expr_name"
    if [ -d "$data_path" ]; then
        resp='q'
        while [[ "$resp" != "y" && "$resp" != "n" ]]; do
            read -p "Data folder exists. Would you like to overwrite? (y/n) " resp;
        done
        if [[ "$resp" == "n" ]]; then
            echo "Preventing overwrite. Exiting";
            exit;
        else
            # Remove the data so that you don't run into any conflicts
            # ssh $click_collector "rm -rf $data_dir/$expr_name/*"
            rm -rf $data_dir/$expr_name/*
        fi
    fi


    # Make the data folder
    mkdir -p "$data_dir/$expr_name"
    # ./nfra/save.sh -d clickrcv --dir "$data_dir/$expr_name"


    # Kill the foundry service cause it acts up when you change routing
    ssh $click_collector "sudo systemctl stop foundryc"
    ssh $click_collector "sudo systemctl stop systemd-timesyncd"
    ssh $click_collector "sudo systemctl stop systemd-networkd"
    # Make sure the vfio drivers are installed correctly
    ssh $click_collector "sudo modprobe vfio"
    ssh $click_collector "sudo modprobe vfio-pci"



    # Set up the recieving connections
    echo "Setting up both recievers"
    ssh $pipe_rcv "sudo ~/rcv-pipe" &
    tap_rcv_pids=()
    for (( j=0; j<${#srvr_tap_array[@]}; j++ )); do
        tap_rcv_pids+=($(./nfra/exe-with-pid.sh -d ${srvr_tap_array[j]} -c "sudo ~/rcv-tap-$j" -n "rcv-pipe-$j.tmp"))
    done



    # Set up pcap on click router
    if [ "$click_collector_uses_tcpdump" = "true" ]; then
        ./init/xdc/tcpdump.sh -s -l "$click_collector" -i "$click_infranet_interface" -w "$click_collector_tcpdump_filename" rm run
    fi

    # Set up pcap recording on filled router
    if [ "$record_filled_pcap" = "true" ]; then
        ./init/xdc/tcpdump.sh -s -l "$filled_router" -i "$filled_interface" -w "$filled_router_pcap_filename" rm run
    fi

    # Set up pcap with pipe gen
    if [ "$pipe_gen_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -s -l "$pipe_gen" -i "$pipe_gen_interface" -w "$pipe_gen_dump_file" rm run
    fi

    # Set up pcap with click gen
    if [ "$click_gen_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -s -l "$click_gen" -i "$click_gen_interface" -w "$click_gen_dump_file" rm run
    fi

    # Set up pcap with pipe rcv
    if [ "$pipe_rcv_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -s -l "$pipe_rcv" -i "$pipe_rcv_interface" -w "$pipe_rcv_dump_file" rm run
    fi

    # Set up pcap on the tapped server
    if [[ "$tap_runs_tcpdump" == "true" ]]; then
        ./init/xdc/tcpdump.sh -s -l "$srvr_tap" -i "$tap_srvr_interface" -w "$srvr_tap_data_file" rm run
    fi
    # Set up pcap on the tapped server
    if [[ "$user_tap_runs_tcpdump" == "true" ]]; then
        ./init/xdc/tcpdump.sh -s -l "$user_tap" -i "$tap_user_interface" -w "$user_tap_data_file" rm run
    fi

    # Set up pcap on the spare interface
    if [[ "$record_spare_pcap" == "true" ]]; then
        ./init/xdc/tcpdump.sh -s -l "$spare_device" -i "$spare_interface" -w "$spare_pcap_file" rm run
    fi



    # Run the click collector (if applicable)
    if [ "$run_click_collector" = "true" ]; then
        # Set up the data collection
        ./nfra/run/clickrcv-router.sh -s -d $click_collector_driver run
        echo "Pausing for click router"
        sleep 10
    fi

    if [ "$run_limiting_router" = "true" ]; then
        ssh routerone "sudo rm -rf ~/data.csv"
        ./nfra/run/enable-shaping.sh -s run
        echo "Pausing for shaping router"
        sleep 10
    fi

    if [ "$run_click_gen_limiting" = "true" ]; then
        ./nfra/run/click-gen-shaping.sh -s run
        echo "Pausing for click gen shaping"
        sleep 10
    fi

    if [ "$run_dpdk_router_two" = "true" ]; then
        ssh $routertwo "sudo rm -rf ~/data.csv"
        ./nfra/run/second-router-limiting.sh -s run
        echo "Pausing for shaping router"
        sleep 10
    fi


    echo "Starting pipe generation"
    # Set up the pipe generation
    # ssh $pipe_gen '~/gen-pipe & echo $!' | tail -n 1 > 'pid-pipe-gen.tmp' &
    pipe_gen_pid=$(./nfra/exe-with-pid.sh -d $pipe_gen -n 'pid-pipe-gen.tmp' -c "~/gen-pipe")


    # Delay the tap starting so we can get some consistent data
    echo "Pausing before initiating tap data client"
    sleep $tap_start_end_delay







    ssh tapuser "ping -i 0.5 -s 850 10.0.5.2" &
    sleep 4
    ssh tapuser $'sudo kill $(ps -e | grep ping | awk \'{print $1}\')'




    tap_pids=()
    echo "Starting tapped client"
    # Start the packet sending
    for (( j=0; j<${#pause_info[@]}; j++ )); do
        # ssh ${user_tap_array[i]} "~/gen-tap-$i & echo \$!" | sudo tee "$data_dir/$expr_name/tapped-sending-info-$i.txt" &
        # tap_pids+=($(./nfra/exe-with-pid.sh -d ${user_tap_array[i]} -c "~/gen-tap-$i" -n 'tap-gen-$i.tmp'))

        IFS=' ' read -r -a info_array <<< "${pause_info[j]}"
	echo "Array: ${pause_info[@]}"
	echo "${info_array[@]}"

        ./nfra/pausing-script.sh --init-delay "${info_array[0]}" --run-time "${info_array[1]}" \
            --pause-time "${info_array[2]}" --pid-file "tap-gen-$j.tmp" \
            --dev "${user_tap_array[j]}" --cmd "~/gen-tap-$j" &

        tap_pids+=($!)

    done



    # Set up killing intervals here


    # Sleep for the duration of the test
    echo "Running test"
    sleep $test_time
    echo "Test Ended"






    for (( j=0; j<${#tap_pids[@]}; j++ )); do
        # ./nfra/kill.sh --server ${user_tap_array[j]} -P ${tap_pids[j]}
        sudo kill ${tap_pids[j]}
        while [ $(ps -e | grep ${tap_pids[j]} | wc -l) -gt 0 ]; do  
            continue
        done;
    done
    for (( j=0; j<${#tap_rcv_pids[@]}; j++ )); do
        ./nfra/kill.sh --server ${srvr_tap_array[j]} -P ${tap_rcv_pids[j]}
    done
 

    # Shut down the stream being tapped
    for (( j=0; j<${#user_tap_array[@]}; j++ )); do
        ssh ${user_tap_array[j]} "sudo ~/gen-destructor-*"
    done
    for (( j=0; j<${#srvr_tap_array[@]}; j++ )); do
        ssh ${srvr_tap_array[j]} "sudo ~/rcv-destructor-*"
    done



    # Delay the tap ending so we can get some consistent data
    echo "Pausing before shutting down pipe"
    sleep $tap_start_end_delay

  


    # Shut down the click router
    if [ "$run_click_collector" = "true" ]; then
        # Force the data dump
        ssh $click_collector 'echo "READ data.dump" | sudo socat - UNIX-CONNECT:/tmp/clicksocket'
        # Stop the router
        ./nfra/run/clickrcv-router.sh stop
        # Save the data
        ./nfra/save.sh -d $click_collector -f $loc_click_datafile -o $click_collector_data_file
    fi

    # Shut down the limiting router
    if [ "$run_limiting_router" = "true" ]; then
        # Stop
        ./nfra/run/enable-shaping.sh stop
        # Save data
        ./nfra/save.sh -d routerone -f "~/data.csv" -o "router-one.csv"
    fi

    # Shut down the click gen router
    if [ "$run_click_gen_limiting" = "true" ]; then
        ./nfra/run/click-gen-shaping.sh stop
    fi

    # Shut down the limiting router
    if [ "$run_dpdk_router_two" = "true" ]; then
        # Stop
        ./nfra/run/second-router-limiting.sh stop
        # Save data
        ./nfra/save.sh -d $routertwo -f "~/data.csv" -o "router-two.csv"
    fi


    # Shut down pcap on click router
    if [ "$click_collector_uses_tcpdump" = "true" ]; then
        ./init/xdc/tcpdump.sh -l "$click_collector" -w "$click_collector_tcpdump_filename" -o "$click_collector_tcpdump_filename" stop save rm
    fi

    # Shut down pcap recording on filled router
    if [ "$record_filled_pcap" = "true" ]; then
        ./init/xdc/tcpdump.sh -l "$filled_router" -w "$filled_router_pcap_filename" -o "$filled_router_pcap_filename" stop save rm
    fi

    # Shut down pcap with pipe gen
    if [ "$pipe_gen_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -l "$pipe_gen" -w "$pipe_gen_dump_file" -o "$pipe_gen_dump_file" stop save rm
    fi

    # Shut down pcap with click gen
    if [ "$click_gen_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -l "$click_gen" -w "$click_gen_dump_file" -o "$click_gen_dump_file" stop save rm
    fi

    # Shut down pcap with pipe rcv
    if [ "$pipe_rcv_cap_dump" = "true" ]; then
        ./init/xdc/tcpdump.sh -l "$pipe_rcv" -w "$pipe_rcv_dump_file" -o "$pipe_rcv_dump_file" stop save rm
    fi

    # Shut down pcap on tapped server
    if [[ "$tap_runs_tcpdump" == "true" ]]; then
        ./init/xdc/tcpdump.sh -l "$srvr_tap" -w "$srvr_tap_data_file" -o "$srvr_tap_data_file" stop save rm
    fi
    if [[ "$user_tap_runs_tcpdump" == "true" ]]; then
        ./init/xdc/tcpdump.sh -l "$user_tap" -w "$user_tap_data_file" -o "$user_tap_data_file" stop save rm
    fi
    # Shut down pcap on the spare interface
    if [[ "$record_spare_pcap" == "true" ]]; then
        ./init/xdc/tcpdump.sh -l "$spare_device" -i "$spare_interface" -w "$spare_pcap_file" -o "$spare_pcap_file" stop save rm
    fi



    scp $config_file clickrcv:~/config-test.sh
    ./nfra/save.sh -d clickrcv -f ~/config-test.sh -o config-test.sh


    # Copy the iperf files & remove if necessary
    if [ "$pipe_uses_iperf3" = true ]; then
        ./nfra/save.sh -d $pipe_rcv -f "~/*$pipe_iperf3_output_file"  \
            -o "pipe-output" --dir $data_dir/$expr_name/pipe-outputs
    fi

    for (( j=0; j<${#tap_uses_iperf3_array[@]}; j++ )); do
        if [ "${tap_uses_iperf3_array[j]}" = true ]; then
            echo "tap iperf3_output_file: ${tap_iperf3_output_file_array[j]}"
            ./nfra/save.sh -d ${srvr_tap_array[j]} -f "~/*${tap_iperf3_output_file_array[j]}"  \
                -o "tap-outputs" --dir "$data_dir/$expr_name/tap-outputs"
        fi
    done



    # For some reason tcpdump isn't being killed on tapsrvr
    for (( j=0; j<${#srvr_tap_array[@]}; j++ )); do
        ./nfra/kill.sh --server ${srvr_tap_array[j]} --regex tcpdump
        ./nfra/kill.sh --server ${user_tap_array[j]} --regex tcpdump
    done

    # Just so the killing processes can complete
    sleep $program_end_delay


    echo "Test completed"


    if [ "$zip" = "true" ]; then
        echo "Zipping pcaps"
        cd $data_dir/$expr_name
        # Might as well zip everything
        zip data *
        # Remove everything EXCEPT ZIPS
        find . -type f ! -name '*.zip' -delete
        cd ../..
    fi

    cd ~/lwt

done

