#!/bin/bash

source ./config-test.sh

TRANSPARENT=true
UNDO_TRANSPARENT=false
DRIVER=$click_collector_driver
# Some basic arg parsing
while [[ $# -gt 0 ]]; do
    case $1 in
        trans)
                TRANSPARENT=true
                UNDO_TRANSPARENT=false
        shift
        ;;
    undo)
        TRANSPARENT=false
        UNDO_TRANSPARENT=true
        shift
        ;;
    esac
done


# ssh pipegen "sudo ip route del 10.0.0.0/24"
# ssh pipegen "sudo ip route del 10.0.1.0/24"
# ssh pipegen "sudo ip route del 10.0.2.0/24"
# ssh pipegen "sudo ip route del 10.0.3.0/24"
# ssh pipegen "sudo ip route del 10.0.4.0/24"
# ssh pipegen "sudo ip route del 10.0.5.0/24"
# ssh pipegen "sudo ip route del 10.0.6.0/24"


ssh $pipe_rcv "sudo ip route del 10.0.0.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.1.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.2.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.3.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.4.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.5.0/24"
ssh $pipe_rcv "sudo ip route del 10.0.6.0/24"


if [ "$TRANSPARENT" = "true" ]; then
  
    # Set up the pipe reciever
    ssh $pipe_rcv "sudo ip route add 10.0.4.0/24 dev $pipe_rcv_interface proto kernel scope link src 10.0.6.2"

    ssh $pipe_rcv "sudo ip route add 10.0.0.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.1.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.2.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.3.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.4.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.5.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.6.0/24 via $click_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"

    # Set up routertwo
    ssh $routertwo "sudo ip route del 10.0.4.0/24"
    ssh $routertwo "sudo ip route del 10.0.6.0/24"
    ssh $routertwo "sudo ip route add 10.0.6.0/24 dev ens1f2 proto kernel scope link src 10.0.4.1"


    # Set up pipegen
    # ssh pipegen "sudo ip route add 10.0.1.0/24 dev $pipe_gen_interface proto kernel scope link src 10.0.0.1"

    # ssh pipegen "sudo ip route add 10.0.0.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.1.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.2.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.3.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.4.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.5.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.6.0/24 via $router_one_gateway_ip dev $pipe_gen_interface protoc static onlink"



    # Set up routerone
    # Since router one is click controlled, we don't need to update the routing table
    # ssh routerone "sudo ip route del 10.0.0.0/24"
    # ssh routerone "sudo ip route add 10.0.0.0/24 dev $router_one_click_interface proto kernel scope link src $router_one_gateway_ip"
fi


if [ "$UNDO_TRANSPARENT" = "true" ]; then
  
    # Set up the pipe reciever
    ssh $pipe_rcv "sudo ip route add 10.0.4.0/24 dev $pipe_rcv_interface proto kernel scope link src 10.0.6.2"

    ssh $pipe_rcv "sudo ip route add 10.0.0.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.1.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.2.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.3.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.4.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.5.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"
    ssh $pipe_rcv "sudo ip route add 10.0.6.0/24 via $pipe_rcv_gateway_ip dev $pipe_rcv_interface protoc static onlink"

    # Set up routertwo
    ssh $filled_router "sudo ip route del 10.0.6.0/24"
    ssh $filled_router "sudo ip route add 10.0.6.0/24 via 10.0.4.2 dev $filled_router_click_interface proto static onlink"

    # ssh pipegen "sudo ip route add 10.0.0.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.1.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.2.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.3.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.4.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.5.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"
    # ssh pipegen "sudo ip route add 10.0.6.0/24 via 10.0.0.2 dev $pipe_gen_interface protoc static onlink"

    # Fix clickgen
    # ssh clickgen "sudo ip route add 10.0.0.0/24 dev ens1f1 proto kernel scope link src 10.0.0.2"
    # ssh clickgen "sudo ip route add 10.0.1.0/24 dev ens1f2 proto kernel scope link src 10.0.1.1"
    # ssh clickgen "sudo ip route add 10.0.0.0/24 via 10.0.0.2 dev ens1f1 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.1.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.2.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.3.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.4.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.5.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
    # ssh clickgen "sudo ip route add 10.0.6.0/24 via 10.0.1.2 dev ens1f2 protoc static onlink"
fi 

