#!/bin/bash

CLIENT="NOTHING"
SERVER="NOTHING"
SERVER_IP="127.0.0.1"
PORT=12345
INTERVAL=0.5
UDP=false
BPS="100M"
TIME=100
OUTPUT="iperf3.res"

# Read through the args
while [[ $# -gt 0 ]]; do
  case $1 in
    -c) # client
        shift
        CLIENT="$1"
        shift
        ;;
    -s) # server
        shift
        SERVER="$1"
        shift
        ;;
    -p) # port
        shift
        PORT="$1"
        shift
        ;;
    -i) # interval
        shift
        INTERVAL="$1"
        shift
        ;;
    -ip) # interval
        shift
        SERVER_IP="$1"
        shift
        ;;
    -u) # udp (or TCP)
        shift
        UDP=true;
        ;;
    -b) 
        shift
        BPS="$1"
        shift
        ;;
    -t) 
        shift
        TIME="$1"
        shift
        ;;
    -o) 
        shift
        OUTPUT="$1"
        shift
        ;;
esac
done

# Dynamically build the server and recv files to a random filename

shebang="#!/bin/bash"

# Make random file names
tmp_gen_file="$(mktemp ~/gen-run.XXXXXXXXX)" || exit 1
tmp_rcv_file="$(mktemp ~/rcv-run.XXXXXXXXX)" || exit 1

chmod +x $tmp_gen_file $tmp_rcv_file

echo $shebang > $tmp_gen_file
echo $shebang > $tmp_rcv_file

# Write the gen file (with or without the UDP flag
if [ "$UDP" = true ]; then
     echo "iperf3 --client $SERVER_IP -p $PORT -u -b $BPS -t $TIME" >> $tmp_gen_file
else
    echo "iperf3 --client $SERVER_IP -p $PORT -b $BPS -t $TIME" >> $tmp_gen_file
fi

# Write the rcv file
# -1 flag specifies to exit after 1 trial is over
echo "iperf3 -s -i $INTERVAL -p $PORT -1 > $OUTPUT" >> $tmp_rcv_file

# Install iperf3 onto the servers
ssh $CLIENT "sudo apt install -y iperf3"
ssh $SERVER "sudo apt install -y iperf3"

# Copy these files to client and server
scp $tmp_gen_file $CLIENT:~/gen
scp $tmp_rcv_file $SERVER:~/rcv

# Remove the files to prevent filesystem polution
rm $tmp_gen_file $tmp_rcv_file

