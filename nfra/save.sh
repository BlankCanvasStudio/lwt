source ./config-test.sh

DEV=''
FILE=''
OUTPUT=''
DIR=''

while [[ $# -gt 0 ]]; do
    case $1 in
        -f) 
            shift
            FILE="$1"
            shift
            ;;

        -o) 
            shift
            OUTPUT="$1"
            shift
            ;;
            
        -d)
           shift
           DEV="$1"
           shift
           ;;

        --dir)
            shift
            DIR="$1"
            shift
            ;;

        *) 
           addr="$1"
           shift
           ;;
    esac
done


if [[ ! "$DIR" = '' ]]; then
    ssh $DEV "sudo mkdir -p $DIR"
fi

if [[ ! "$FILE" = '' ]]; then

    # Make sure we own the file
    ssh $DEV "sudo chown $(whoami) $FILE"
    # ssh $DEV "sudo chown $(whoami):$(whoami) $FILE"

    ssh $DEV "sudo mkdir -p $data_dir/$expr_name"

    # Send the data to the server
    # scp $DEV:"$FILE" "$data_dir/$expr_name/$click_collector_data_file"
    # ssh $DEV "cp $FILE $(whoami)@$data_server:\"$data_dir/$expr_name/$FILE\""
    if [[ ! "$OUTPUT" = '' ]]; then
        # ssh $DEV "sudo cp -av $FILE $data_dir/$expr_name/$OUTPUT"
        scp $DEV:$FILE $data_dir/$expr_name/$OUTPUT
    else
        # ssh $DEV "sudo cp -av $FILE $data_dir/$expr_name/$FILE"
        scp $DEV:$FILE $data_dir/$expr_name/$FILE
    fi

    # Remove the data (so it doesn't mess with next experiment)
    ssh $DEV "sudo rm $FILE"

fi
