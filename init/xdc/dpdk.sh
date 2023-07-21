#!/bin/bash

for target in "$@"; do
    scp ./init/loc/dpdk.sh $target:~/dpdk.sh
    scp ./nfra/bind.sh $target:~/bind.sh
    ssh $target 'sudo ~/dpdk.sh'
done

