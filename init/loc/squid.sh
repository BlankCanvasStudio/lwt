#!/bin/bash

sudo apt-get update

sudo apt-get -y install squid

echo "http_access allow mynetwork" >> /etc/squid/squid.conf
echo "acl mynetwork src 10.0.5.2/24" >> /etc/squid/squid.conf

sudo systemctl start squid

