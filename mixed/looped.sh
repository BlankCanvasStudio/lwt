#!/bin/bash

# Define an array
my_array=(
    # Need to add some verifications for this to verified it runs
    'gdoc-basic-writing-youtube-ads'


    'scp-rsync'
    'twitch-curl-https'
    'twitch-iperf-100K'
    'twitch-iperf-10K'
    'twitch-ping-5s-350B'
    'twitch-ping-2s-350B'
    'twitch-wget-ftp-large'
    'wget-ftp-large-wget-short'
    'wget-https-large-wget-short'
    'youtube-curl-https'
    'youtube-iperf-100K'
    'youtube-iperf-10K'
    'youtube-ping-2s-350B'
    'youtube-ping-5s-350B'
    'youtube-wget-ftp-large'
    'stutter/wget-ftp-large-youtube'
    # 'stutter/wget-ftp-large-scp'
    # 'stutter/wget-ftp-large-gdocs'
)

# Iterate over the elements in the array
for element in "${my_array[@]}"; do
    echo "Building $element"
    ./mixed/build.sh -c "./scenarios/mixed/$element/config.sh"
    echo "Running Experiment: $element"
    # Please specify repitions in config file
    ./mixed/run.sh -c "./scenarios/mixed/$element/config.sh"
    # Save data in git repo
    pushd .
    cd ../data-lwt
    git add --ignore-removal *
    git commit -m "Create data for $element"
    git push
    rm -r ./*
    ssh tapsrvr "rm -rf --interactive=never /tmp/*"
    ssh tapuser "rm -rf --interactive=never /tmp/*"
    ssh tapsrvr 'rm ~/*'
    ssh tapuser 'rm ~/*'
    popd
    ssh tapsrvr "rm /tmp/*"
    sleep 360
done

