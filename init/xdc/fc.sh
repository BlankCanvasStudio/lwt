#!/bin/bash

source ./config-test.sh


echo "Building fast click"

FORCE=false;
if [[ "$1" == "-f" ]]; then
    FORCE=true;
    shift;
fi

for target in "$@"; do
    echo "compile() {" > ./tmp-click-config
    echo "./configure $click_config" >> ./tmp-click-config
    echo        "make -j 12" >> ./tmp-click-config
    echo "}" >> ./tmp-click-config

    echo "Copying files over"
    scp ./init/loc/fc.sh $target:~/fastclick.sh
    scp ./init/resources/dpdk-element.cpp $target:~/dpdk-element.cpp
    scp $click_collector_object_c_files $target:~
    scp ./nfra/bind.sh $target:~/bind.sh
    scp ./tmp-click-config $target:~/click-config.sh
    echo "Actually building fastclick"
    if [ "$FORCE" = "true" ]; then
        echo "Removing fc directories and starting over"
        ssh $target 'sudo ~/fastclick.sh -f'
    else 
        ssh $target 'sudo ~/fastclick.sh'
    fi
    rm ./tmp-click-config
done

