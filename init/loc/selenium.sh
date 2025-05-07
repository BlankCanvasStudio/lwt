#!/bin/bash

# Set up to install chrome
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' 
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Remove all the duplicates
awk '!seen[$0]++' /etc/apt/sources.list.d/google-chrome.list | sudo tee /etc/apt/sources.list.d/google-chrome.list > /dev/null

sudo apt update

sudo apt -y install firefox

sudo apt -y install google-chrome-stable 

sudo apt -y install python3-pip

pip3 install -y selenium

wget https://addons.mozilla.org/firefox/downloads/file/4198829/ublock_origin-1.54.0.xpi \
    -O ~/ublock.xpi

