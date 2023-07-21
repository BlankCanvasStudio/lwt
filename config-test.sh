#!/bin/bash

# This doubles as the folder where data will be generated in data/
export expr_name="expr5"

# The names you'd like to give the files of the recorded data
export srvr_tap_data_file="srvr_tap.pcap"
export pipe_rcv_data_file="pipe_rcv.csv"

# How long to wait to start the tapped server
export tap_start_end_delay=1
# How long to run the experiment for
export test_time=5


# Hosts generation pipe for experiment
export pipe_gen=pipegen
export pipe_rcv=pipercv
# Files the hosts execute. Need to be able to run these with the syntax ./filename
export pipe_gen_exe="./nfra/generation/basic-socket/pipe/gen.py"
export pipe_rcv_exe="./nfra/generation/basic-socket/pipe/rcv.py"

# Hosts to be tapped
export user_tap=tapuser
export srvr_tap=tapsrvr
# Files the hosts execute. Need to be able to run these with the syntax ./filename
export tap_gen_exe="./nfra/generation/basic-socket/tap/gen.py"
export tap_rcv_exe="./nfra/generation/basic-socket/tap/rcv.py"


# This is all the info relating to the click data collector
export click_collector=clickrcv
export dpdk_interface="eth2"
export router_file="./nfra/collection/timestamping-router/recorder.cpp"
# There are 2 (.cc and .hh). We always need to refer to both so use *
# The object this generates should be called DataRecorder
#     If it isn't, you need to update recorder.cpp
# This can be extended to include all files in a folder if need be
export click_collector_object_c_files="./nfra/collection/click-timestamper/timestamprecorder.*"

# \/ Needs to be in agreement with where the click-router is 
#   outputting its data (so also determined by recorder.cpp)
export loc_click_datafile="~/data.csv"

# This is a static file, no need to parameterize it
# export bind_script="./infra/bind.sh"

