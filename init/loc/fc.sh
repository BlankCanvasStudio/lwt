#!/bin/bash

source ./click-config.sh

if [[ "$1" == "-f" ]]; then
    echo "Removing old fastclick files"
    sudo rm -rf ./fastclick
fi


if [[ "$1" == "recomp" ]]; then
    cd fastclick
    compile
    exit
fi

sudo apt update && sudo apt upgrade -y

sudo apt install -y git

sudo apt install -y build-essential

sudo apt install -y autoconf

sudo apt install -y dpdk-dev
git clone https://github.com/tbarbette/fastclick.git

mv ./dpdk-element.cpp ./fastclick/elements/userlevel/fromdpdkdevice.cc
mv ./*.cc ./fastclick/elements/local
mv ./*.hh ./fastclick/elements/local

cd fastclick
chmod +x ./deps.sh
sudo ./deps.sh
compile
echo 'export PATH="$PATH:~/fastclick/bin"' >> ~/.bashrc

