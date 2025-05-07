#!/bin/bash

# Install dependencies
sudo apt-get update 
sudo apt install -y git
sudo apt install -y build-essential

# Install new mt beta of iperf
git clone https://github.com/esnet/iperf.git
cd iperf
# Switch to multi-threading beta
git checkout mt

sudo ./configure
sudo make -j 12
sudo make install

ldconfig

# Default install location should be: /usr/local/bin/iperf3
# If its not install there, iperf is install via apt which isn't good

