#!/bin/bash

source ./config-test.sh

DRIVER=$limiting_router_driver 
SILENT=true

run() {
    # Running the router (not building)
    ./nfra/update/resolve.conf.sh $limiting_router
    # echo "Writing /etc/resolv.conf"
    # ssh $limiting_router "sudo rm /etc/resolv.conf"
    # ssh $limiting_router "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
    # ssh $limiting_router "echo 'search metal.init.lwt' | sudo tee -a /etc/resolv.conf"
    # Turn off systemd-timesyncd
    ssh $limiting_router "sudo systemctl stop systemd-timesyncd"
    # Install policyket-1 so systemd doesn't run into permission error
    ssh $limiting_router "sudo apt install -y policykit-1"
    # Kill the foundry service cause it acts up when you change routing
    ssh $limiting_router "sudo systemctl stop foundryc"
    ssh $limiting_router "sudo systemctl stop systemd-timesyncd"
    ssh $limiting_router "sudo systemctl stop systemd-networkd"


    # Set the links down
    # ssh routerone "sudo ip link set $interfaceon down"
    # ssh routerone "sudo ip link set $interfacetwo down"
    #
    # Set up the data collection
    echo "Running the limiting"

    # Make sure the interface is bound
    ssh $limiting_router "~/bind.sh -p -d $DRIVER ens1f1" # Don't mute in case
    ssh $limiting_router "~/bind.sh -p -d $DRIVER ens1f2" # Bind the internet interface as well
    ssh $limiting_router "~/bind.sh -p -d $DRIVER ens1f3" # Bind the internet interface as well


    if [ "$SILENT" = true ]; then
        # Running with chtr -r 99 makes this way worse
        ssh $limiting_router "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $limiting_router_core_mask -n $limiting_router_net_lanes" &
    else
        ssh $limiting_router "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $limiting_router_core_mask -n $limiting_router_net_lanes"
    fi
}

update() {
    scp $limiting_router_file $limiting_router:"~/router.cpp"
}

stop-router() {
    # Shut down the router
    echo "Shutting down Limiting Router"

    if [ "$limiting_router_uses_tcpdump" = "true" ]; then
        ./nfra/kill.sh --server $limiting_router --regex "tcpdump"
    else
        ./nfra/kill.sh --server $limiting_router --regex "click"
    fi
    
}

edit() {
    vim $limiting_router_file
}


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
            echo "Unknown argument passed into ./nfra/run/enable-shaping.sh. Quitting"
        exit
    esac
done

