#!/bin/bash

# Revision tag: c8a73080f46c0a8628ab8014d6d53c90801ec3d5

# Limit at rate 100000000b burst 1500B limit 1500KB

# This doubles as the folder where data will be generated in data/
export expr_name_base="gtranslate-french-lorem-reversed" # Sim number gets added automatically
# export data_dir="/mnt/stor0/searchlight/lwt" # so you don't need to keep the data in the same repo
export data_dir="../data-lwt" # so you don't need to keep the data in the same repo

export repititions=200 # How many trials to run

# Do you want to zip pcaps and other helpful pcap info (very helpful)
export zip=true
export tcpdump_buff_size=16384
# Set the pcap snap len size (how much packet is captured)
# Set to 0 if you want max
export snap_len=60 # We just care about time stamp and orig len, don't need packet



# How long to wait to start the tapped server
export tap_start_end_delay=10
# How long to run the experiment for
export test_time=150
# How long to pause at the end for
export program_end_delay=0



# info on link you're trying to fill
export filled_router=routertwo
export filled_interface=ens1f3
export filled_router_click_interface=ens1f2
# Should you record pcap at that link?
export record_filled_pcap=false
export filled_router_pcap_filename="filled-router.pcap"


# info on link you're trying to fill
export record_spare_pcap=false
export spare_device=routertwo
export spare_interface=ens1f2
export spare_pcap_file="filled-router-out.pcap"


# Hosts generation pipe for experiment
# export pipe_gen=routertwo
export pipe_gen=pipegen
export pipe_rcv=pipercv
# Files the hosts execute. Need to be able to run these with the syntax ./filename
export pipe_gen_exe="./nfra/generation/basic-socket/pipe/adv/gen.py"
export pipe_rcv_exe="./nfra/generation/basic-socket/pipe/adv/rcv.py"
# Set these options if you want to use iperf3 over a custom program
export pipe_uses_iperf3=true
export pipe_iperf3_port=12345
export pipe_iperf3_interval=0.5 # corresponds to -i flag
export pipe_iperf3_udp=true # Use UDP or TCP data
# NOTE ON BANDWIDTH: If its exactly the same as your link, 
#   data loss increases. Having higher than is much more consistent
export pipe_iperf3_bps=100M # Bandwidth you want 
export pipe_iperf3_length=1448B # This option didn't exist in best case
export pipe_iperf3_pacing=0.000 # smaller values should make traffic smoother (in ms)
export pipe_iperf3_fq_rate=0
export pipe_iperf3_parallel=1 # the -P flag in iperf itself
export pipe_iperf3_copies=1 # Manually creating multiple iperf instances to run in parallel
export pipe_iperf3_server_ip="10.0.6.2"
export pipe_iperf3_output_file="pipe-iperf3.res"


# Should we limit via clickgen
# This didn't exist in best case
export run_click_gen_limiting=false
export click_gen_device="clickgen"
export click_gen_router="./nfra/shaping/click-gen/router.cpp"
export click_gen_net_lanes=16
export click_gen_core_mask=FFFFFFFFFFF
# So the device works in transparent mode
export pipe_gen_interface="ens1f3"
export router_one_click_interface="ens1f3"
export pipe_gen_gateway_ip="10.0.0.1"
export router_one_gateway_ip="10.0.1.1"



# Creating tcpdump on pipe gen
export pipe_gen_cap_dump=false
export pipe_gen_dump_file="pipe-gen.pcap"
export pipe_gen_interface="ens1f3"
# Creating tcpdump on click gen
export click_gen=clickgen
export click_gen_cap_dump=false
export click_gen_dump_file="click-gen.pcap"
export click_gen_interface="ens1f2"
# Creating tcpdump on pipe rcv
export pipe_rcv_cap_dump=false
export pipe_rcv_dump_file="pipe-rcv.pcap"
export pipe_rcv_interface="ens1f3"



# Hosts to be tapped
# export user_tap=routertwo
export user_tap=tapsrvr
export srvr_tap=tapuser
# Files the hosts execute. Need to be able to run these with the syntax ./filename
export tap_gen_build="./init/loc/selenium.sh"
export tap_rcv_build="./nfra/generation/empty.sh"
export tap_gen_exe="./scenarios/websites/gtranslate/french-lorem/translate.py"
export tap_rcv_exe="./nfra/generation/empty.sh"
# Set these options if you want to use iperf3 over a custom program
export tap_uses_iperf3=false
export tap_iperf3_port=12345
export tap_iperf3_interval=0.5 # corresponds to -i flag
export tap_iperf3_udp=true # Use UDP or TCP data
# NOTE ON BANDWIDTH: If its exactly the same as your link, 
#   data loss increases. Having higher than is much more consistent
export tap_iperf3_bps=50K # Bandwidth you want
export tap_iperf3_length=8000B
export tap_iperf3_pacing=0.001 # smaller values should make traffic smoother (in ms)
export tap_iperf3_parallel=1
export tap_iperf3_copies=1
export tap_iperf3_fq_rate=0
export tap_iperf3_server_ip="10.0.5.2"
export tap_iperf3_output_file="tap-iperf3.res"
export tap_runs_tcpdump=true
export tap_srvr_interface="ens1f3" # What interface you'd like to dump
# The names you'd like to give the files of the recorded data
export srvr_tap_data_file="srvr_tap.pcap"
export tap_gen_destructor="./scenarios/websites/destructor.sh"
export tap_rcv_destructor="./nfra/generation/empty.sh"





# This is all the info relating to the click data collector
export click_collector=clickrcv
export run_click_collector=true
export click_collector_data_file="pipe_rcv.csv"
export click_collector_pipe_rcv_interface="ens1f3"
export click_collector_infranet_interface="ens1f2"

export click_collector_uses_pci_addressing=false
export click_collector_infranet_pci="0000:81:00.2"
export click_collector_pipe_rcv_pci="0000:81:00.3"
export click_collector_driver="vfio-pci"
export click_collector_core_mask="FFFFFFFFFFF" # Got 0.006ms
export click_collector_net_lanes="16"

export router_file="./nfra/collection/minimal/erik/router.cpp"
export click_collector_object_c_files="./nfra/collection/click-timestamper/erik-opt/*"



# This is so we can run tcpdump over click stuff for debug
export click_collector_uses_tcpdump=false
export click_collector_tcpdump_filename='clickrcv-dump.pcap'

# In case you need to change this value
export pipe_rcv_gateway_ip="10.0.6.1"
export click_rcv_gateway_ip="10.0.4.1"


# These options allow you to control the limiting router link
#       Currently thats routerone
export run_limiting_router=true
export limiting_router="routerone"
export limiting_router_file="./nfra/shaping/no-click-gen-r1/shapper.cpp"
export limiting_router_net_lanes=16
export limiting_router_core_mask=FFFFFFFFFFF


# Should we run dpdk on router two?
export run_dpdk_router_two=false
export routertwo="routertwo"
export routertwo_file="./nfra/shaping/routertwo/router.cpp"
export routertwo_net_lanes=16
export routertwo_core_mask=FFFFFFFFFFF


# \/ Needs to be in agreement with where the click-router is 
#   outputting its data (so also determined by recorder.cpp)
export loc_click_datafile="~/data.csv"

# Should we resolve all tapuser requests internally??
export tap_user_resolve_via_tapsrvr=false
export tap_user_resolve_via_tapuser=true

# Used for testing & documenting different click builds
export click_config='--enable-dpdk --enable-dpdk-pool --disable-bpf --enable-bound-port-transfer --enable-local --enable-intel-cpu --disable-batch --enable-select=poll CFLAGS="-O3" CXXFLAGS="-std=c++11 -O3" --enable-user-multithread --enable-multithread --enable-dpdk-packet'

