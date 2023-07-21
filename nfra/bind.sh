#!/bin/bash
sudo su -c "echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages" root
sudo ip link set $1 down
sudo modprobe uio_pci_generic
pci_addr=$(sudo dpdk-devbind.py --status | awk "/$1/ {print \$1}")
sudo dpdk-devbind.py --bind=uio_pci_generic $pci_addr
echo ""
echo ""
echo ""
sudo dpdk-devbind.py --status
