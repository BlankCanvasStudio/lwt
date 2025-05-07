#!/bin/bash


# foundryc.service
# systemd-networkd.service
setup () {
    echo "Installing tapsrvr"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapsrvr
    # Update everything
    ssh tapsrvr "sudo apt update -y && sudo apt upgrade -y"
    # Install IP tables
    ssh tapsrvr "sudo apt -y install iptables"
    # Add forwarding to larger internet interface 
    ssh tapsrvr "sudo iptables -t nat -A POSTROUTING -o infranet -j MASQUERADE"
    # ssh tapsrvr "sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    # Make sure forwarding is enabled
    echo "injecting"
    ssh tapsrvr 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    echo "finished injecting"
    ssh tapsrvr "sudo sysctl -p"


    echo ""
    echo ""
    echo ""
    echo "Installing router two"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routertwo
    # Update everything
    ssh routertwo "sudo apt update -y && sudo apt upgrade -y"
    # Make it into a router through 10.0.5.1 and not infra
    ssh routertwo "sudo apt -y install iptables"
    ssh routertwo "sudo iptables -t nat -A POSTROUTING -o ens1f1 -j MASQUERADE"
    # ssh routertwo "sudo iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE"
    ssh routertwo 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    ssh routertwo "sudo sysctl -p"
    # Delete default route on router two
    ssh routertwo "sudo ip route del default via 172.30.0.1"
    # Add default route through tapsrvr
    ssh routertwo "sudo ip route add default via 10.0.5.2 dev ens1f1 proto dhcp src 10.0.5.1"
    # ssh routertwo "sudo ip route add default via 10.0.5.2 dev eth3 proto dhcp src 10.0.5.1"
    ssh routertwo "sudo ip route del default via 172.29.0.1"


    echo ""
    echo ""
    echo ""
    echo "Installing router one"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routerone
    # Update everything
    ssh routerone "sudo apt update -y && sudo apt upgrade -y"
    # Add forwarding to routertwo interface so tapuser can access greater internet
    ssh routerone "sudo apt -y install iptables"
    ssh routerone "sudo iptables -t nat -A POSTROUTING -o ens1f1 -j MASQUERADE"
    # ssh routerone "sudo iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE"
    ssh routerone 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    ssh routerone "sudo sysctl -p"
    # Delete default route on router one
    ssh routerone "sudo ip route del default via 172.29.0.1"
    ssh routerone "sudo ip route add default via 10.0.3.2 dev ens1f1 proto dhcp src 10.0.3.1"
    ssh routerone "sudo ip route del default via 172.30.0.1"
    # Add default route through routertwo
    # ssh routerone "sudo ip route add default via 10.0.3.2 dev eth3 proto dhcp src 10.0.3.1"


    echo ""
    echo ""
    echo ""
    echo "Installing tauser"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapuser
    # Update everything
    ssh tapuser "sudo apt update -y && sudo apt upgrade -y"
    # Delete default route on tapuser
    ssh tapuser "sudo ip route del default via 172.30.0.1"
    ssh tapuser "sudo ip route del default via 172.29.0.1"
    # Add default route through routerone
    ssh tapuser "sudo ip route add default via 10.0.2.1 dev ens1f3 proto dhcp src 10.0.2.2"
    # ssh tapuser "sudo ip route add default via 10.0.2.1 dev eth1 proto dhcp src 10.0.2.2"
}



takedown() {
    echo "Undoing tapsrvr"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapsrvr
    # Remove the old default routes and bring new one
    ssh tapsrvr "sudo ip route add default via 172.30.0.1 dev infranet proto dhcp src 172.30.0.17 metric 512" 
    ssh tapsrvr "sudo ip route add default via 172.29.0.1 dev ens2np0 proto dhcp src 172.29.0.44 metric 1024"
    ssh tapsrvr "sudo ip route del default via 10.0.5.1"


    echo ""
    echo ""
    echo ""
    echo "Undoing router two"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routertwo
    # Remove the old default routes and bring new one
    ssh routertwo "sudo ip route add default via 172.30.0.1 dev infranet proto dhcp src 172.30.0.16 metric 512" 
    ssh routertwo "sudo ip route add default via 172.29.0.1 dev ens2np0 proto dhcp src 172.29.0.62 metric 1024"
    ssh routertwo "sudo ip route del default via 10.0.5.2"
    ssh routertwo "sudo ip route del default via 10.0.2.2"
    ssh routertwo "sudo ip route del default via 10.0.3.1"

    echo ""
    echo ""
    echo ""
    echo "Installing router one"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routerone
    # Remove the old default routes and bring new one
    ssh routerone "sudo ip route add default via 172.30.0.1 dev infranet proto dhcp src 172.30.0.15 metric 512" 
    ssh routerone "sudo ip route add default via 172.29.0.1 dev ens2np0 proto dhcp src 172.29.0.59 metric 1024"
    ssh routerone "sudo ip route del default via 10.0.3.2"
    ssh routerone "sudo ip route del default via 10.0.2.2"


    echo ""
    echo ""
    echo ""
    echo "Installing tap user"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapuser
    # Remove the old default routes and bring new one
    ssh tapuser "sudo ip route del default via 10.0.2.1"
    ssh tapuser "sudo ip route add default via 172.30.0.1 dev infranet proto dhcp src 172.30.0.18 metric 512" 
    ssh tapuser "sudo ip route add default via 172.29.0.1 dev ens2np0 proto dhcp src 172.29.0.18 metric 1024"
}



# foundryc.service
# systemd-networkd.service
reverse() {
    echo "Installing tap user"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapuser
    # Update everything
    ssh tapuser "sudo apt update -y && sudo apt upgrade -y"
    # Install IP tables
    ssh tapuser "sudo apt -y install iptables"
    # Add forwarding to larger internet interface 
    ssh tapuser "sudo iptables -t nat -A POSTROUTING -o infranet -j MASQUERADE"
    # ssh tapsrvr "sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    # Make sure forwarding is enabled
    echo "injecting"
    ssh tapuser 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    echo "finished injecting"
    ssh tapuser "sudo sysctl -p"


    echo ""
    echo ""
    echo ""
    echo "Installing router one"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routerone
    # Update everything
    ssh routerone "sudo apt update -y && sudo apt upgrade -y"
    # Make it into a router through 10.0.5.1 and not infra
    ssh routerone "sudo apt -y install iptables"
    ssh routerone "sudo iptables -t nat -A POSTROUTING -o ens1f2 -j MASQUERADE"
    # ssh routerone "sudo iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE"
    ssh routerone 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    ssh routerone "sudo sysctl -p"
    # Delete default route on router two
    ssh routerone "sudo ip route del default via 172.30.0.1"
    # Add default route through tapsrvr
    ssh routerone "sudo ip route add default via 10.0.2.2 dev ens1f2 proto dhcp src 10.0.2.1"
    # ssh routerone "sudo ip route add default via 10.0.5.2 dev eth3 proto dhcp src 10.0.5.1"
    ssh routerone "sudo ip route del default via 172.29.0.1"


    echo ""
    echo ""
    echo ""
    echo "Installing router two"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh routertwo
    # Update everything
    ssh routertwo "sudo apt update -y && sudo apt upgrade -y"
    # Add forwarding to routertwo interface so tapuser can access greater internet
    ssh routertwo "sudo apt -y install iptables"
    ssh routertwo "sudo iptables -t nat -A POSTROUTING -o ens1f3 -j MASQUERADE"
    # ssh routertwo "sudo iptables -t nat -A POSTROUTING -o eth3 -j MASQUERADE"
    ssh routertwo 'if [[ "$(tail -n 1 /etc/sysctl.conf)" != "net.ipv4.ip_forward=1" ]]; then echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf; fi'
    ssh routertwo "sudo sysctl -p"
    # Delete default route on router one
    ssh routertwo "sudo ip route del default via 172.29.0.1"
    ssh routertwo "sudo ip route add default via 10.0.3.1 dev ens1f3 proto dhcp src 10.0.3.2"
    ssh routertwo "sudo ip route del default via 172.30.0.1"
    # Add default route through routertwo
    # ssh routertwo "sudo ip route add default via 10.0.3.2 dev eth3 proto dhcp src 10.0.3.1"


    echo ""
    echo ""
    echo ""
    echo "Installing tap srvr"
    # Make sure resolve.conf is up and running
    ./nfra/update/resolve.conf.sh tapsrvr
    # Update everything
    ssh tapsrvr "sudo apt update -y && sudo apt upgrade -y"
    # Delete default route on tapsrvr
    ssh tapsrvr "sudo ip route del default via 172.30.0.1"
    ssh tapsrvr "sudo ip route del default via 172.29.0.1"
    # Add default route through routerone
    ssh tapsrvr "sudo ip route add default via 10.0.5.1 dev ens1f3 proto dhcp src 10.0.5.2"
    # ssh tapsrvr "sudo ip route add default via 10.0.2.1 dev eth1 proto dhcp src 10.0.2.2"
}


SETUP=false
TAKEDOWN=false
REVERSE=false


while [[ $# -gt 0 ]]; do
     case $1 in
         setup) 
             setup
             shift
             ;;
             
         takedown)
            takedown
            shift
            ;;

         reverse)
            reverse
            shift
            ;;
        *)
            echo "Unexpected argument in nfra/kill. Quitting"
            exit
    esac
done


