#!/bin/bash

echo "Building dpdk"

for target in "$@"; do
    echo "Copying files over"
    scp ./init/loc/dpdk.sh $target:~/dpdk.sh
    scp ./nfra/bind.sh $target:~/bind.sh
    echo "Running build"
    ssh $target 'sudo ~/dpdk.sh'
done

