#!/bin/bash

# Do some light cli parsing
USE_PCI=false
DRIVER="uio_pci_generic"
addr='eth1'

while [[ $# -gt 0 ]]; do
     case $1 in
         -p) 
             USE_PCI=true
             shift
             ;;
             
         -d)
            shift
            DRIVER="$1"
            shift
            ;;
         *) 
            echo here $1
            addr="$1"
            shift
            ;;
    esac
done

sudo su -c "echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages" root

sudo ip link set $addr down

sudo modprobe uio_pci_generic
sudo modprobe vfio
sudo modprobe vfio-pci

if [ "$USE_PCI" = true ]; then
    sudo dpdk-devbind.py --bind=$DRIVER $addr
else
    pci_addr=$(sudo dpdk-devbind.py --status | awk "/$addr/ {print \$1}")
    echo pci_addr: $pci_addr
    sudo ip link set $addr down
    sudo dpdk-devbind.py --bind=$DRIVER $pci_addr
fi
echo ""
echo ""
echo ""
sudo dpdk-devbind.py --status
