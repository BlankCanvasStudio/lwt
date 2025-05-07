#!/bin/bash

# Install ftp library
pip install pyftpdlib
sudo pip install pyftpdlib

# Write random file
filename="rand-file"
rm $filename
dd if=/dev/urandom of=$filename bs=1M count=10000

