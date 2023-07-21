#!/bin/bash

source ./config-test.sh

for target in "$@"; do
    scp ./init/loc/fc.sh $target:~/fastclick.sh
    scp $click_collector_object_c_files $target:~
    scp ./nfra/bind.sh $target:~/bind.sh
    ssh $target 'sudo ~/fastclick.sh'
done

