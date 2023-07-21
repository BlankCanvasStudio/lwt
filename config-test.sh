#!/bin/bash

# This doubles as the folder where data will be generated in data/
export expr_name="expr3"

# The names you'd like to give the files of the recorded data
export srvr_tap_data_file="srvr_tap.pcap"
export pipe_rcv_data_file="pipe_rcv.csv"


# Hosts generation pipe for experiment
export pipe_gen=pipegen
export pipe_rcv=pipercv
# Files the hosts execute
export pipe_gen_exe="./nfra/generation/basic-socket/pipe/gen.py"
export pipe_rcv_exe="./nfra/generation/basic-socket/pipe/rcv.py"

# Hosts to be tapped
export user_tap=tapuser
export srvr_tap=tapsrvr
# Files the hosts execute
export tap_gen_exe="./nfra/generation/basic-socket/tap/gen.py"
export tap_rcv_exe="./nfra/generation/basic-socket/tap/rcv.py"


# This is all the info relating to the click data collector
export click_collector=clickrcv
export dpdk_interface="eth1"
export router_file="./nfra/collection/click-timestamper/timestamping-recorder/recorder.cpp"
# There are 2 (.cc and .hh). We always need to refer to both so use *
# The object this generates should be called DataRecorder
#     If it isn't, you need to update recorder.cpp
export click_collector_object_c_files="./nfra/collection/click-timestamper/timestamprecorder.*"

export tap_start_end_delay=1
export test_time=5

# \/ Needs to be in agreement with where the click-router is 
#   outputting its data (so also determined by recorder.cpp)
export loc_click_datafile="~/data.csv"

# This is a static file, no need to parameterize it
# export bind_script="./infra/bind.sh"

