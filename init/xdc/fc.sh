#!/bin/bash

source ./config-test.sh
echo "Building fast click"
for target in "$@"; do
    echo "Copying files over"
    scp ./init/loc/fc.sh $target:~/fastclick.sh
    scp $click_collector_object_c_files $target:~
    scp ./nfra/bind.sh $target:~/bind.sh
    echo "Installing gcc"
    echo "Actually building fastclick"
    ssh $target 'sudo ~/fastclick.sh'
done

