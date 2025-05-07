#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git

# Necessary for ./boot
sudo apt install -y libtool
sudo apt-get install -y autoconf

sudo apt-get install -y libcap-ng-dev

git clone https://github.com/openvswitch/ovs.git

cd ovs

./boot.sh

./configure --with-dpdk=static
#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install -y git

# Necessary for ./boot
sudo apt install -y libtool
sudo apt-get install -y autoconf

sudo apt-get install -y libcap-ng-dev

git clone https://github.com/openvswitch/ovs.git

cd ovs

./boot.sh

./configure --with-dpdk=static

