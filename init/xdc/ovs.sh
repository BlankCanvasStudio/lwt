#!/bin/bash

echo "Building ovs"

for target in "$@"; do
    echo "Copying files over"
    scp ./init/loc/ovs.sh $target:~/ovs.sh
    echo "Actually building ovs"
    ssh $target 'sudo ~/ovs.sh'
done

