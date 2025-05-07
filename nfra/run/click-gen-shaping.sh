#!/bin/bash

source ./config-test.sh

DRIVER=$click_gen_device_driver 
SILENT=false

run() {
    # Running the router (not building)
    ./nfra/update/resolve.conf.sh $click_gen_device
    # echo "Writing /etc/resolv.conf"
    # ssh $click_gen_device "sudo rm /etc/resolv.conf"
    # ssh $click_gen_device "echo 'nameserver 172.30.0.1' | sudo tee -a /etc/resolv.conf"
    # ssh $click_gen_device "echo 'search metal.init.lwt' | sudo tee -a /etc/resolv.conf"
    # Turn off systemd-timesyncd
    ssh $click_gen_device "sudo systemctl stop systemd-timesyncd"
    # Install policyket-1 so systemd doesn't run into permission error
    ssh $click_gen_device "sudo apt install -y policykit-1"
    # Kill the foundry service cause it acts up when you change routing
    ssh $click_gen_device "sudo systemctl stop foundryc"
    ssh $click_gen_device "sudo systemctl stop systemd-timesyncd"
    ssh $click_gen_device "sudo systemctl stop systemd-networkd"


    # Set up the data collection
    echo "Running the limiting"

    # Make sure the interface is bound
    ssh $click_gen_device "~/bind.sh -d $DRIVER ens1f2" # Bind the internet interface as well
    ssh $click_gen_device "~/bind.sh -d $DRIVER ens1f3" # Bind the internet interface as well


    if [ "$SILENT" = true ]; then
        # Running with chtr -r 99 makes this way worse
        ssh $click_gen_device "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $click_gen_core_mask -n $click_gen_net_lanes" &
    else
        ssh $click_gen_device "cd ~; sudo ~/fastclick/bin/click ~/router.cpp --dpdk -c $click_gen_core_mask -n $click_gen_net_lanes"
    fi
}

update() {
    scp $click_gen_router $click_gen_device:"~/router.cpp"
}

stop-router() {
    # Shut down the router
    echo "Shutting down Limiting Router"
    ./nfra/kill.sh --server $click_gen_device --regex "click"
}

edit() {
    vim $click_gen_router 
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
            echo "Unknown argument passed into ./nfra/run/click-gen-shaping.sh. Quitting"
        exit
    esac
done

