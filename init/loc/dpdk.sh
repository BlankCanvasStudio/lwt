#!/bin/bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y meson

sudo apt-get install -y git

sudo apt install -y build-essential

sudo apt-get install -y python3-pyelftools

sudo apt install -y libnuma-dev

echo 1024 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# This is so the .so files that are installed are globally linkable
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/x86_64-linux-gnu' >> $install_dir/.bashrc

# Make sure the root user also has access to the updated path
sudo su -c "echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/x86_64-linux-gnu' >> /root/.bashrc"

sudo apt install -y dpdk
sudo apt install -y dpdk-dev

sudo modprobe uio_pci_generic

sudo apt install -y lshw

