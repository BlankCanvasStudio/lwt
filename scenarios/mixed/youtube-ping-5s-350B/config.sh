#!/bin/bash

# This doubles as the folder where data will be generated in data/
# export expr_name="erik-opt-with-ping-100M-03"
export expr_name_base="mixed-youtube-ping-5s-350B"
export data_dir="../data-lwt"
# Saving this value for later
export expr_name_mix=$expr_name_base

export repititions=200 # How many trials to run

config_files=(
    'scenarios/ping-5s-350B/config-test.sh'
    'scenarios/websites-reversed/youtube/astley/config-test.sh'
)

# (How long until you turn it on, how long it should run for, and how long it should pause for)
pause_info=(
    '0 100 0'
    '0 100 0'
)

# Strip the information for each of the tap configs from each of the files. The pipe config will 
# be taken from first specified file. Because of this, we will need to iterate the files in 
# reverse order and source them (to make my life easier)

# Here are all the parameters we need from each file
user_tap_array=()
srvr_tap_array=()

tap_gen_build_array=()
tap_rcv_build_array=()

tap_gen_exe_array=()
tap_rcv_exe_array=()

tap_gen_destructor_array=()
tap_rcv_destructor_array=()

tap_uses_iperf3_array=()
tap_iperf3_port_array=()
tap_iperf3_interval_array=()
tap_iperf3_udp_array=()
tap_iperf3_bps_array=()
tap_iperf3_length_array=()
tap_iperf3_pacing_array=()
tap_iperf3_parallel_array=()
tap_iperf3_copies_array=()
tap_iperf3_fq_rate_array=()
tap_iperf3_server_ip_array=()
tap_iperf3_output_file_array=()


for (( i=${#config_files[@]}-1; i>=0; i-- )); do

    source "${config_files[i]}"

    user_tap_array+=($user_tap)
    srvr_tap_array+=($srvr_tap)
    tap_gen_build_array+=($tap_gen_build)
    tap_rcv_build_array+=($tap_rcv_build)
    tap_gen_exe_array+=($tap_gen_exe)
    tap_rcv_exe_array+=($tap_rcv_exe)
    tap_gen_destructor_array+=($tap_gen_destructor)
    tap_rcv_destructor_array+=($tap_rcv_destructor)
    tap_uses_iperf3_array+=($tap_uses_iperf3)
    tap_iperf3_port_array+=($tap_iperf3_port)
    tap_iperf3_interval_array+=($tap_iperf3_interval)
    tap_iperf3_udp_array+=($tap_iperf3_udp)
    tap_iperf3_bps_array+=($tap_iperf3_bps)
    tap_iperf3_length_array+=($tap_iperf3_length)
    tap_iperf3_pacing_array+=($tap_iperf3_pacing)
    tap_iperf3_parallel_array+=($tap_iperf3_parallel)
    tap_iperf3_copies_array+=($tap_iperf3_copies)
    tap_iperf3_fq_rate_array+=($tap_iperf3_fq_rate)
    tap_iperf3_server_ip_array+=($tap_iperf3_server_ip)
    tap_iperf3_output_file_array+=($tap_iperf3_output_file + "-$i")

done


# Load this value back so the experiment is named properly
export expr_name_base=$expr_name_mix



# Some gobal configs you can specify yourself. If the option you're looking for isn't here, use
# the first listed config file

export tap_user_resolve_via_tapsrvr=false
export tap_user_resolve_via_tapuser=true


# Do you want to zip pcaps and other helpful pcap info (very helpful)
export zip=true
export tcpdump_buff_size=16384
# Set the pcap snap len size (how much packet is captured)
# Set to 0 if you want max
export snap_len=192 # We just care about time stamp and orig len, don't need packet


# How long to wait to start the tapped server
export tap_start_end_delay=10
# How long to run the experiment for
export test_time=35
# How long to pause at the end for
export program_end_delay=0


# info on link you're trying to fill
export record_spare_pcap=false
export spare_device=routertwo
export spare_interface=ens1f2
export spare_pcap_file="filled-router-out.pcap"


# Creating tcpdump on pipe gen
export pipe_gen_cap_dump=false
export pipe_gen_dump_file="pipe-gen.pcap"
# export pipe_gen_interface="eth1"
export pipe_gen_interface="ens1f3"
# Creating tcpdump on click gen
export click_gen=clickgen
export click_gen_cap_dump=false
export click_gen_dump_file="click-gen.pcap"
# export click_gen_interface="eth1"
export click_gen_interface="ens1f2"
# Creating tcpdump on pipe rcv
export pipe_rcv_cap_dump=false
export pipe_rcv_dump_file="pipe-rcv.pcap"
export pipe_rcv_interface="ens1f3"


# tcpdump on tapuser
export user_tap_runs_tcpdump=false
export tap_user_interface="ens1f3" # What interface you'd like to dump
export user_tap_data_file="user_tap.pcap"


# tcpdump on tapsrvr
export tap_runs_tcpdump=true
export tap_srvr_interface="ens1f3" # What interface you'd like to dump
export srvr_tap_data_file="srvr_tap.pcap"

