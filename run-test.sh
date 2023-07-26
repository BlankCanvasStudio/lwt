#!/bin/bash


# Import the config settings so everything is easy to manage
source ./config-test.sh


# Verify that the folder doesn't already exist
data_path="./data/$expr_name"
if [ -d "$data_path" ]; then
    resp = 'q'
    while [[ "$resp" != "y" && "$resp" != "n" ]]; do
        read -p "Data folder exists. Would you like to overwrite? (y/n) " resp;
    done
    if [[ "$resp" == "n" ]]; then
        echo "Preventing overwrite. Exiting";
	exit;
    else
        # Remove the data so that you don't run into any conflicts
        rm -f $data_path/*
    fi
fi


# Set up the recieving connections
echo "Setting up both recievers"
ssh $pipe_rcv "~/rcv" &
ssh $srvr_tap "~/rcv" &


# Set up the data collection
./nfra/run-router.sh -s


echo "Starting TCP recording on tapped server"
# Remove the old tcpdump
ssh $srvr_tap "rm -f ~/$srvr_tap_data_file"
# Start the TCP-dump (-U prevents buffering so it can be killed)
ssh $srvr_tap "cd ~; sudo tcpdump -U -i eth1 -w ~/$srvr_tap_data_file" &


echo "Starting pipe generation"
# Set up the pipe generation
ssh $pipe_gen "~/gen" &

# Delay the tap starting so we can get some consistent data
echo "Pausing before initiating tap data client"
sleep $tap_start_end_delay

echo "Starting tapped client"
# Start the packet sending
ssh $user_tap "~/gen" > "./data/$expr_name/tapped-sending-info.txt" &





# Sleep for the duration of the test
echo "Running test"
sleep $test_time
echo "Test Ended"





# Shut down the stream being tapped
if [ "$tap_uses_iperf3" = false ]; then
    # Get the pid of the genprocess and then kill it
    echo "Killing tapped client"
    gen_pid=$(ssh $user_tap "pgrep -o gen")
    ssh $user_tap "kill $gen_pid"
    # Get the pid of the rcv process and then kill it
    echo "Killing tapped server"
    rcv_pid=$(ssh $srvr_tap "pgrep -o rcv")
    ssh $srvr_tap "kill $rcv_pid"
fi



# Delay the tap ending so we can get some consistent data
echo "Pausing before shutting down pipe"
sleep $tap_start_end_delay



# Shut down the pipe-gen process
if [ "$pipe_uses_iperf3" = false ]; then
    # Get the pid of the gen process and then kill it
    echo "Killing pipe gen process"
    gen_pid=$(ssh $pipe_gen "pgrep -o gen")
    ssh $pipe_gen "kill $gen_pid"
    # Get the pid of the rcv process and then kill it
    echo "Killing pipe rcv process"
    rcv_pid=$(ssh $pipe_rcv "pgrep -o rcv")
    ssh $pipe_rcv "kill $rcv_pid"
fi


# Shutting down click router
./nfra/close-router.sh

# Shut down the TCPdump
echo "Shutting down TCP recording on tapped server"
tcpdump_pid=$(ssh $srvr_tap "pgrep -o tcpdump")
ssh $srvr_tap "sudo kill $tcpdump_pid"



# Save the data
echo "Saving collected data to data/$expr_name"
mkdir -p "./data/$expr_name"
scp $srvr_tap:"~/$srvr_tap_data_file" "./data/$expr_name/$srvr_tap_data_file"
scp $click_collector:"$loc_click_datafile" "./data/$expr_name/$pipe_rcv_data_file"
# Write a copy of the config to the folder. Makes life easier
cp "./config-test.sh" "./data/$expr_name"

# Remove the data from the experiment infra
echo "Removing data files from the infrastructure"
ssh $srvr_tap "rm -f ~/$srvr_tap_data_file"
ssh $click_collector "rm -f $loc_click_datafile"

# Copy the iperf files & remove if necessary
if [ "$pipe_uses_iperf3" = true ]; then
    scp $pipe_rcv:~/$pipe_iperf3_output_file "./data/$expr_name/$pipe_iperf3_output_file"
    ssh $pipe_rcv "rm -f ~/$pipe_iperf3_output_file"
fi
if [ "$tap_uses_iperf3" = true ]; then
    scp $srvr_tap:~/$tap_iperf3_output_file "./data/$expr_name/$tap_iperf3_output_file"
    ssh $srvr_tap "rm -f ~/$tap_iperf3_output_file"
fi


echo "Rewriting /etc/resolv.conf"
ssh $click_collector "sudo rm /etc/resolv.conf"
ssh $click_collector "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
ssh $click_collector "echo 'search build.init.lwt' | sudo tee -a /etc/resolv.conf"

echo "Test completed"


