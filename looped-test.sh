#!/bin/bash

# Define an array
my_array=("baseline" "1M" "100K" "10K" 
            "ping-2s-15B" "ping-2s-35B" "ping-2s-350B" "ping-2s-850B"
                          "ping-5s-35B" "ping-5s-350B" "ping-5s-850B"
            "gen/f-iperf30-h-iperf30" "gen/f-iperf40-h-iperf40"
            "gen/f-ping-400B-3s-h-iperf-100M" "gen/f-ping-400B-3s-h-iperf-80M"
            "wget" "wget/google" "wget/reddit" "wget/wikipedia"    # "wget-squid-websites" 
            "scp-linux" # "proxy-selenium-squid-websites" 
            "websites/amazon/add-to-cart" "websites/amazon/browse-front"
            "websites/facebook/default-route" "websites/facebook/login-page"
            "websites/gdocs/basic-writing" "websites/gdocs/diff-acc-listen-to-writing" 
                "websites/gdocs/diff-accc-basic-writing-with-listen" 
                "websites/gdocs/same-acc-listen-to-writing"
            "websites/gmail/basic-recieving" "websites/gmail/basic-sending"
            "websites/google/basic-search"
            "websites/gtranslate/basic-lorem" "websites/gtranslate/french-lorem"
            "websites/twitch/basic-streamer-view" "websites/twitch/view-home"
            "websites/youtube/astley" "websites/youtube/ad-block/astley"
            

            "wget-reversed" "wget-reversed/google" "wget-reversed/reddit" "wget-reversed/wikipedia" 
            "file-transfer/curl/ftp" "file-transfer/curl/http" "file-transfer/curl/https"
            "file-transfer/ftp"
            "file-transfer/git"
            "file-transfer/rsync"
            "file-transfer/scp"
            "file-transfer/wget/ftp" "file-transfer/wget/http" "file-transfer/wget/https"

            "websites-reversed/amazon/add-to-cart" "websites-reversed/amazon/browse-front"
            "websites-reversed/facebook/default-route" "websites-reversed/facebook/login-page"
            "websites-reversed/gdocs/basic-writing" "websites-reversed/gdocs/diff-acc-listen-to-writing" 
                "websites-reversed/gdocs/diff-accc-basic-writing-with-listen" 
                "websites-reversed/gdocs/same-acc-listen-to-writing"
            "websites-reversed/gmail/basic-recieving" "websites-reversed/gmail/basic-sending"
            "websites-reversed/google/basic-search"
            "websites-reversed/gtranslate/basic-lorem" "websites-reversed/gtranslate/french-lorem"
            "websites-reversed/twitch/basic-streamer-view" "websites-reversed/twitch/view-home"
            "websites-reversed/youtube/astley" "websites-reversed/youtube/ad-block/astley"


            "tcp/curl/ftp" "tcp/curl/http" "tcp/curl/https"
            "tcp/ftp"
            "tcp/git"
            "tcp/git"
            "tcp/google/basic-search"
            "tcp/gtranslate/basic-lorem" "tcp/gtranslate/french-lorem"
            "tcp/ping-2s-350B" "tcp/ping-2s-35B"
            "tcp/ping-5s-850B" "tcp/ping-5s-35B"
            "tcp/rsync" "tcp/scp"
            "tcp/twitch/basic-streamer-view" 
            "tcp/twitch/view-home" 
            "tcp/youtube/astley"
            "tcp/youtube/ad-block/astley"
            "tcp/wget/ftp" "tcp/wget/http" "tcp/wget/https"
        )

# Can't do discord cause bot detection
#             "websites/discord/basic-chat" "websites/discord/load-old-chats"

# Iterate over the elements in the array
for element in "${my_array[@]}"; do
    echo "Building $element"
    ./build-test.sh -c "./scenarios/$element/config-test.sh"
    echo "Running Experiment: $element"
    # Please specify repitions in config file
    ./run-test.sh -c "./scenarios/$element/config-test.sh"
    # Save data in git repo
    pushd .
    cd ../data-lwt
    git add --ignore-removal *
    git commit -m "Create data for $element"
    git push
    rm -r ./*
    rm -rf --interactive=never 


    ssh tapsrvr "rm -rf --interactive=never /tmp/*"
    ssh tapuser "rm -rf --interactive=never /tmp/*"
    ssh tapsrvr 'rm ~/*'
    ssh tapuser 'rm ~/*'
    popd
    sleep 360
done

