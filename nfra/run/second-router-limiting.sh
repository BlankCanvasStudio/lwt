#!/bin/bash

source ./config-test.sh

DRIVER=$click_collector_driver 
SILENT=true

run() {
    # Running the router (not building)
    ./nfra/update/resolve.conf.sh $routertwo
    # echo "Writing /etc/resolv.conf"
    # ssh $routertwo "sudo rm /etc/resolv.conf"
    # ssh $routertwo "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
    # ssh $routertwo "echo 'search metal.init.lwt' | sudo tee -a /etc/resolv.conf"
    # Turn off systemd-timesyncd
    ssh $routertwo "sudo systemctl stop systemd-timesyncd"
    # Install policyket-1 so systemd doesn't run into permission error
    ssh $routertwo "sudo apt install -y policykit-1"
    # Kill the foundry service cause it acts up when you change routing
    ssh $routertwo "sudo systemctl stop foundryc"
    ssh $routertwo "sudo systemctl stop systemd-timesyncd"
    ssh $routertwo "sudo systemctl stop systemd-networkd"

    # Set up the data collection
    echo "Running the limiting"

    # Make sure the interface is bound
    ssh $routertwo "~/bind.sh -d $DRIVER ens1f1" # Don't mute in case
    ssh $routertwo "~/bind.sh -d $DRIVER ens1f2" # Bind the internet interface as well
    ssh $routertwo "~/bind.sh -d $DRIVER ens1f3" # Bind the internet interface as well


    if [ "$SILENT" = true ]; then
        # Running with chtr -r 99 makes this way worse
        ssh $routertwo "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $limiting_router_core_mask -n $limiting_router_net_lanes" &
    else
        ssh $routertwo "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $limiting_router_core_mask -n $limiting_router_net_lanes"
    fi
}

update() {
    scp $routertwo_file $routertwo:"~/router.cpp"
}

stop-router() {
    # Shut down the router
    echo "Shutting down Limiting Router"

    if [ "$click_collector_uses_tcpdump" = "false" ]; then
        ./nfra/kill.sh --server $routertwo --regex "click"
    else
        ./nfra/kill.sh --server $routertwo --regex "tcpdump"
    fi
    
}

edit() {
    vim $routertwo_file
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
            echo "Unknown argument passed into ./nfra/run/router.sh. Quitting"
        exit
    esac
done

