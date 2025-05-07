#!/bin/bash

source ./config-test.sh

SERVER="NOTHING"
INTERFACE=lo
FILE_NAME="tmp.pcap"
OUTPUT_FILE="./data/tmp.pcap"
RUN=true
KILL=false
SAVE=false
BACKGROUND=false
SERVER_FILE='tmp.pcap'



run() {
    echo "Recording pcap on $SERVER"
    if [ $BACKGROUND = "true" ]; then
        ssh $SERVER "cd ~; sudo tcpdump -B $tcpdump_buff_size -s $snap_len --immediate-mode -U -i $INTERFACE -w ~/$SERVER_FILE" &
    else 
        ssh $SERVER "cd ~; sudo tcpdump -B $tcpdump_buff_size -s $snap_len --immediate-mode -U -i $INTERFACE -w ~/$SERVER_FILE"
    fi
}

stop() {
    echo "Shutting fown TCP recording on $INTERFACE"
    tcpdump_pid=$(ssh $server "pgrep -o tcpdump")
    ssh $SERVER "sudo kill $tcpdump_pid"
    # Trying it a second way just in case
    ./nfra/kill.sh --server $SERVER --regex "tcpdump"
}

save() {
    ./nfra/save.sh -d $SERVER -f "~/$SERVER_FILE" -o "$OUTPUT_FILE"
    # scp $SERVER:"~/$SERVER_FILE" "$OUTPUT_FILE"
}

remove() {
     ssh $SERVER "rm ~/$SERVER_FILE"
}
 


# Read through the args
while [[ $# -gt 0 ]]; do
  case $1 in
    -l) # client
        shift
        SERVER="$1"
        shift
        ;;
    -i) # interface
        shift
        INTERFACE="$1"
        shift
        ;;
    -w) # filename to save to
        shift
        SERVER_FILE="$1"
        shift
        ;;
    -o) # output file to save to
        shift
        OUTPUT_FILE="$1"
        shift
        ;;
    -s)
        BACKGROUND="true"
        shift
        ;;
    -b)
        BACKGROUND="true"
        shift
        ;;
    stop)
        RUN="false"
        KILL="true"
        shift
        ;;
    run)
        run
        shift
        ;;
    save)
        save
        shift
        ;;
    rm) 
        remove
        shift
        ;;
    *)
        echo "Unexpected argument in init/xdc/tcpdump. Quitting"
        exit
esac
done

