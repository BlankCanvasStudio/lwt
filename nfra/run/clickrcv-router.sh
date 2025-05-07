#!/bin/bash

source ./config-test.sh

# Ordering is done like this so you can edit, update, and run in a single command
edit() {
    vim $router_file
}

update() {
    scp $router_file $click_collector:"~/router.cpp"
}


run() {
    # Running the router (not building)
    ./nfra/update/resolve.conf.sh $click_collector
    # echo "Writing /etc/resolv.conf"
    # ssh $click_collector "sudo rm /etc/resolv.conf"
    # ssh $click_collector "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
    # ssh $click_collector "echo 'search metal.init.lwt' | sudo tee -a /etc/resolv.conf"
    # Turn off systemd-timesyncd
    ssh $click_collector "sudo systemctl stop systemd-timesyncd"
    # Install policyket-1 so systemd doesn't run into permission error
    ssh $click_collector "sudo apt install -y policykit-1"
    # Kill the foundry service cause it acts up when you change routing
    ssh $click_collector "sudo systemctl stop foundryc"
    ssh $click_collector "sudo systemctl stop systemd-timesyncd"
    ssh $click_collector "sudo systemctl stop systemd-networkd"

    # Set the links down
    ssh $click_collector "sudo ip link set $click_infranet_interface down"
    ssh $click_collector "sudo ip link set $click_pipe_rcv_interface down"

    # This didn't work. Fuck my whole life
    # Increase the max process count cause thats been an issue
    # echo "Increasing max process count"
    # sudo ulimit -u 1200000 # Hella 4 gud luck

    # Set up the data collection
    echo "Starting click data collector"
    # Remove the old data from the click collector
    ssh $click_collector "rm -f $loc_click_datafile"
    # Make sure the interface is bound
    if [ "$click_collector_uses_pci_addressing" = "false" ]; then
        ssh $click_collector "~/bind.sh -d $DRIVER $click_collector_pipe_rcv_interface" # Don't mute in case
        ssh $click_collector "~/bind.sh -d $DRIVER $click_collector_infranet_interface" # Bind the internet interface as well
    else    
        ssh $click_collector "~/bind.sh -d $DRIVER -p $click_collector_pipe_rcv_pci" # Don't mute in case
        ssh $click_collector "~/bind.sh -d $DRIVER -p $click_collector_infranet_pci" # Bind the internet interface as well
    fi
    # Start the click router
    if [ "$SILENT" = true ]; then
        # Running with chtr -r 99 makes this way worse
        ssh $click_collector "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $click_collector_core_mask -n $click_collector_net_lanes" &
    else
        # Running with chtr -r 99 makes this way worse
        ssh $click_collector "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $click_collector_core_mask -n $click_collector_net_lanes"
    fi
}

stop-router() {
    # Shut down the router
    echo "Shutting down Click Router"

    if [ "$click_collector_uses_tcpdump" = "false" ]; then
        ./nfra/kill.sh --server $click_collector --regex "click"
    else
        ./nfra/kill.sh --server $click_collector --regex "tcpdump"
    fi
    
}

delete() {
    echo "Deleting click data"
    ssh $click_collector "sudo rm -rf $loc_click_datafile"
}

SILENT=false
DRIVER=$click_collector_driver
# Some basic arg parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        run)
            run
            shift
            ;;
        stop)
            stop-router
            shift
            ;;
        update)
            update
            shift
            ;;
        edit)
            edit
            shift
            ;;
        del)
            delete
            shift
            ;;
        -s) 
            SILENT=true
            shift
            ;;
        -d)
            shift
            DRIVER="$1"
            shift
            ;;
        *)
            echo "Unknown argument passed into ./nfra/run/router.sh. Quitting"
        exit
    esac
done

