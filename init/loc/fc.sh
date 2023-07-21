#!/bin/bash

compile() {

./configure --enable-dpdk --enable-intel-cpu --verbose --enable-select=poll CFLAGS="-O3" CXXFLAGS="-std=c++11 -O3"  --disable-dynamic-linking --enable-poll --enable-bound-port-transfer --enable-local --enable-flow --disable-task-stats --disable-cpu-load
make

}

if [[ "$1" == "recomp" ]]; then
    cd fastclick
    compile
    exit
fi

if [ ! -f "./timestamprecorder.cc" ]; then
    echo "Cannot find timestamprecorder.cc. Quitting"
    exit
fi

if [ ! -f "./timestamprecorder.hh" ]; then
    echo "Cannot find timestamprecorder.hh. Quitting"
    exit
fi


sudo apt update && sudo apt upgrade -y

sudo apt install -y git

sudo apt install -y build-essential

git clone https://github.com/tbarbette/fastclick.git

sudo apt install -y dpdk-dev

mv ./timestamprecorder.cc ./timestamprecorder.hh ./fastclick/elements/local

cd fastclick
compile
chmod +x ./deps.sh
sudo ./deps.sh
echo 'export PATH="$PATH:~/fastclick/bin"' >> ~/.bashrc

