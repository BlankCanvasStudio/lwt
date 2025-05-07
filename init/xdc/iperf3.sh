#!/bin/bash

CLIENT="NOTHING"
SERVER="NOTHING"
SERVER_IP="127.0.0.1"
PORT=12345
INTERVAL=0.5
UDP=false
BPS="100M"
LENGTH="8000B"
TIME=100
OUTPUT="iperf3.res"
PACING_TIMER=1
PARALLEL=1
COPIES=1
FAIR_QUEUE=0
NAME=""

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
    -pt) # pacing timer
        shift
        PACING_TIMER="$1"
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
    -P)
        shift
        PARALLEL="$1"
        shift
        ;;
    -fq)
        shift
        FAIR_QUEUE="$1"
        shift
        ;;
    -x)
        shift
        COPIES="$1"
        shift
        ;;
    -n)
        shift
        NAME="$1"
        shift
        ;;
    -l)
        shift
        LENGTH="$1"
        shift
        ;;
    *)
        echo "Unexpected argument in init/xdc/iperf3. Quitting"
        exit
    esac
done

# Remove all old gen & rcv files

ssh $CLIENT "sudo rm ~/gen$NAME"
ssh $CLIENT "sudo rm ~/gen$NAME-*"

ssh $SERVER "sudo rm ~/rcv$NAME"
ssh $SERVER "sudo rm ~/rcv$NAME-*"



# Dynamically build the server and recv files to a random filename

shebang="#!/bin/bash"

# Iterate over number of parallel clients to create and generate
#       scripts which 
for (( i = 0; i < $COPIES; i++ )); do

    echo "Creating parallel connection #$i"
    # Make random file names
    tmp_gen_file="$(mktemp ~/gen-run.XXXXXXXXX)" || exit 1
    tmp_rcv_file="$(mktemp ~/rcv-run.XXXXXXXXX)" || exit 1

    chmod +x $tmp_gen_file $tmp_rcv_file

    echo $shebang > $tmp_gen_file
    echo $shebang > $tmp_rcv_file

    # Write the gen file (with or without the UDP flag
    if [ "$UDP" = true ]; then
        echo "iperf3 --client $SERVER_IP -4 -P $PARALLEL -p $(($PORT+i)) -b $BPS -t $TIME --pacing-timer $PACING_TIMER --fq-rate $FAIR_QUEUE -u" >> $tmp_gen_file
        # echo "iperf3 --client $SERVER_IP --length $LENGTH -4 -p $(($PORT+i)) -b $BPS -t $TIME --pacing-timer $PACING_TIMER --fq-rate $FAIR_QUEUE -u" >> $tmp_gen_file
    else
        echo "iperf3 --client $SERVER_IP -4 -P $PARALLEL -p $(($PORT+i)) -b $BPS -t $TIME --pacing-timer $PACING_TIMER --fq-rate $FAIR_QUEUE"    >> $tmp_gen_file
        # echo "iperf3 --client $SERVER_IP --length $LENGTH -4 -p $(($PORT+i)) -b $BPS -t $TIME --pacing-timer $PACING_TIMER --fq-rate $FAIR_QUEUE"    >> $tmp_gen_file
    fi

    # Write the rcv file
    # -1 flag specifies to exit after 1 trial is over
    echo "iperf3 -s -i $INTERVAL -p $(($PORT+i)) -1" >> $tmp_rcv_file

    # Copy these files to client and server
    scp $tmp_gen_file $CLIENT:"~/gen$NAME-$i"
    scp $tmp_rcv_file $SERVER:"~/rcv$NAME-$i"

    # Remove the files to prevent filesystem polution
    rm $tmp_gen_file $tmp_rcv_file

done


# Create the larger files which call all the sub files 
#       (ie parallel connections)
tmp_gen_file="$(mktemp ~/gen-run.XXXXXXXXX)" || exit 1
tmp_rcv_file="$(mktemp ~/rcv-run.XXXXXXXXX)" || exit 1

chmod +x $tmp_gen_file $tmp_rcv_file

echo $shebang > $tmp_gen_file
echo $shebang > $tmp_rcv_file

for (( i = 0; i < $COPIES; i++ )); do

    echo "./gen$NAME-$i &" >> $tmp_gen_file;
    echo "./rcv$NAME-$i >> $i-$pipe_iperf3_output_file &" >> $tmp_rcv_file;

done

# Copy these files to client and server
scp $tmp_gen_file $CLIENT:"~/gen$NAME"
scp $tmp_rcv_file $SERVER:"~/rcv$NAME"

# Remove the files to prevent filesystem polution
rm $tmp_gen_file $tmp_rcv_file

# Install iperf3 onto the servers
# ssh $CLIENT "sudo apt install -y iperf3"
# ssh $SERVER "sudo apt install -y iperf3"

# Manually build iperf3 on the servers
scp init/loc/iperf.sh $CLIENT:"~/build-iperf.sh"
scp init/loc/iperf.sh $SERVER:"~/build-iperf.sh"

ssh $CLIENT "sudo ~/build-iperf.sh"
ssh $SERVER "sudo ~/build-iperf.sh"

# ssh $CLIENT "sudo rm ~/build-iperf.sh"
# ssh $SERVER "sudo rm ~/build-iperf.sh"

