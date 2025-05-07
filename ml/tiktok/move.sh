#!/bin/bash

# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/baseline-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/baseline-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/0-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-listen-to-writing-diff-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-listen-to-writing-diff-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/1-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-google-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name number=$(basename "$folder" | sed 's/wget-google-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/2-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-multiple-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-multiple-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/3-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/regular-wget-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/regular-wget-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/4-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/scp-linux-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/scp-linux-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/5-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-wikipedia-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-wikipedia-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/6-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/facebook-default-route-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/facebook-default-route-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/7-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/iperf-1M-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/iperf-1M-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/8-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/iperf-100K-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/iperf-100K-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/9-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/iperf-10K-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/iperf-10K-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/10-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-2s-15B-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-2s-15B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/11-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-5s-35B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-5s-35B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/12-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-2s-350B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-2s-350B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/13-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-2s-850B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-2s-850B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/14-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-5s-350B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-5s-350B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/15-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/ping-5s-850B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/ping-5s-850B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/16-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/f-iperf-30M-h-iperf-30M-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/f-iperf-30M-h-iperf-30M-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/17-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/f-iperf-40M-h-iperf-40M-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/f-iperf-40M-h-iperf-40M-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/18-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/f-ping-400B-3s-h-iperf-100M-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/f-ping-400B-3s-h-iperf-100M-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/19-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/f-ping-400B-3s-h-iperf-80M-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/f-ping-400B-3s-h-iperf-80M-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/20-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/amazon-add-to-cart-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/amazon-add-to-cart-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/21-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/amazon-browse-front-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/amazon-browse-front-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/22-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-basic-writing-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-basic-writing-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/23-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-listen-to-writing-same-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-listen-to-writing-same-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/24-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-listen-\&-writing-diff-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-listen-\&-writing-diff-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/25-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gmail-basic-recieving-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gmail-basic-recieving-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/26-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gmail-basic-sending-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gmail-basic-sending-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/27-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/astley-youtube-adblock-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/astley-youtube-adblock-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/28-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/astley-youtube-raw-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/astley-youtube-raw-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/29-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/google-basic-search-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/google-basic-search-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/30-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gtranslate-basic-lorem-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gtranslate-basic-lorem-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/31-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gtranslate-french-lorem-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gtranslate-french-lorem-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/32-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/twitch-basic-streamer-view-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/twitch-basic-streamer-view-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/33-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/twitch-view-home-*; do
# 
#     if [[ $folder == *reversed* ]]; then
#         continue
#     fi
# 
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/twitch-view-home-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/34-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-multiple-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-multiple-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/35-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/amazon-add-to-cart-reversed*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/amazon-add-to-cart-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/36-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/amazon-browse-front-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/amazon-browse-front-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/37-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/astley-youtube-adblock-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/astley-youtube-adblock-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/38-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/facebook-default-route-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/facebook-default-route-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/39-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-basic-writing-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-basic-writing-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/40-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gdocs-listen-to-writing-diff-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gdocs-listen-to-writing-diff-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/41-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gmail-basic-recieving-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gmail-basic-recieving-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/42-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gmail-basic-sending-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gmail-basic-sending-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/43-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/google-basic-search-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/google-basic-search-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/44-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gtranslate-basic-lorem-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gtranslate-basic-lorem-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/45-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/gtranslate-french-lorem-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/gtranslate-french-lorem-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/46-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-wikipedia-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-wikipedia-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/47-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/twitch-basic-streamer-view-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/twitch-basic-streamer-view-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/48-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-gdoc-basic-writing-youtube-ads-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-gdoc-basic-writing-youtube-ads-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/49-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-scp-rsync-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-scp-rsync-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/50-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-curl-https-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-curl-https-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/51-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-iperf-100K-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-iperf-100K-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/52-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-stutter-wget-ftp-large-scp-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-stutter-wget-ftp-large-scp-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/53-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-wget-ftp-large-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-wget-ftp-large-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/54-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-wget-ftp-large-wget-short-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-wget-ftp-large-wget-short-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/55-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-wget-https-large-wget-short-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-wget-https-large-wget-short-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/56-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# for folder in ../../../data-lwt/mixed-stutter-wget-ftp-large-youtube-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-stutter-wget-ftp-large-youtube-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/57-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-ping-2s-350B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-ping-2s-350B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/58-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-stutter-wget-ftp-large-gdocs-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-stutter-wget-ftp-large-gdocs-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/59-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/true-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/true-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/60-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/curl-https-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/curl-https-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/61-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-https-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-https-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/62-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
#  # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/curl-http-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/curl-http-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/63-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-http-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-http-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/64-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/git-linux-from-github-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/git-linux-from-github-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/65-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/rsync-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/rsync-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/66-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/scp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/scp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/67-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/wget-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/wget-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/68-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-ping-5s-350B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-ping-5s-350B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/69-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/mixed-twitch-iperf-10K-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/mixed-twitch-iperf-10K-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/70-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-curl-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-curl-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/71-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-curl-http-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-curl-http-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/72-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-wget-http-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-wget-http-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/73-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/curl-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/curl-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/74-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-twitch-view-home-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-twitch-view-home-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/75-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-twitch-basic-streamer-view-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-twitch-basic-streamer-view-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/76-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-true-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-true-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/77-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-scp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-scp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/78-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-rsync-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-rsync-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/79-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-ping-5s-850B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-ping-5s-850B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/80-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-ping-5s-35B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-ping-5s-35B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/81-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-ping-2s-350B-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-ping-2s-350B-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/82-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-gtranslate-french-lorem-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-gtranslate-french-lorem-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/83-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-gtranslate-basic-lorem-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-gtranslate-basic-lorem-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/84-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-google-basic-search-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-google-basic-search-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/85-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-git-linux-from-github-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-git-linux-from-github-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/86-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-curl-https-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-curl-https-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/87-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-wget-https-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-wget-https-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/88-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-astley-youtube-raw-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-astley-youtube-raw-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/89-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-wget-ftp-rand-data-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-wget-ftp-rand-data-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/90-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done
# 
# # Loop through folders with the name format baseline-<some number>
# for folder in ../../../data-lwt/tcp-astley-youtube-adblock-reversed-*; do
#     # Get the number part of the folder name
#     number=$(basename "$folder" | sed 's/tcp-astley-youtube-adblock-reversed-\([0-9]*\)/\1/')
#     
#     # Create the destination folder name
#     dest_folder="./cw-ow-timing-class/data/91-$number"
# 
#     mkdir -p $dest_folder
#     
#     # Copy the contents of the folder to the destination
#     cp -r "$folder"/* "$dest_folder"
# done


for folder in ./cw-ow-timing-class/data/*; do
    rm -rf $folder
done 

trial_num=0

# Loop through folders with the name format baseline-<some number>
trial_name=amazon-add-to-cart-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))


trial_name=amazon-add-to-cart-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))


trial_name=amazon-browse-front-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))


trial_name=amazon-browse-front-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=astley-youtube-adblock-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=astley-youtube-adblock-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=astley-youtube-raw-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=astley-youtube-raw-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=baseline-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=curl-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=curl-http-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=curl-https-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=facebook-default-route-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=facebook-default-route-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=f-iperf-30M-h-iperf-30M-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=f-iperf-40M-h-iperf-40M-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=f-ping-400B-3s-h-iperf-100M-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=f-ping-400B-3s-h-iperf-80M-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-basic-writing-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-basic-writing-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-to-writing-diff-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-to-writing-diff-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-to-writing-same-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-to-writing-same-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-\&-writing-diff-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gdocs-listen-\&-writing-diff-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=git-linux-from-github-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gmail-basic-recieving-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gmail-basic-recieving-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gmail-basic-sending-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gmail-basic-sending-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=google-basic-search-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=google-basic-search-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gtranslate-basic-lorem-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gtranslate-basic-lorem-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gtranslate-french-lorem-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=gtranslate-french-lorem-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=iperf-100K-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=iperf-10K-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=iperf-1M-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-2s-15B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-2s-350B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-2s-35B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-2s-850B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-5s-350B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-5s-35B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=ping-5s-850B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=rsync-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=scp-linux-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=scp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-astley-youtube-adblock-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-astley-youtube-raw-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-curl-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-curl-http-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-curl-https-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-git-linux-from-github-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-google-basic-search-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-gtranslate-basic-lorem-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-gtranslate-french-lorem-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-ping-2s-350B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-ping-2s-35B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-ping-5s-35B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-ping-5s-850B-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-rsync-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-scp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-true-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-twitch-basic-streamer-view-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-twitch-view-home-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-wget-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-wget-http-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=tcp-wget-https-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=true-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=twitch-basic-streamer-view-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=twitch-basic-streamer-view-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=twitch-view-home-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=twitch-view-home-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-ftp-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-google-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-google-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-http-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-https-rand-data-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-multiple-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-multiple-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-reddit-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-reddit-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-wikipedia-reversed-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))

trial_name=wget-wikipedia-with-ping-start
for folder in ../../../data-lwt/$trial_name-*; do
    # Get the number part of the folder name
    number=$(basename "$folder" | sed 's/.*-\([0-9]*\)$/\1/')
    
    # Create the destination folder name
    dest_folder="./cw-ow-timing-class/data/$trial_num-$number"

    mkdir -p $dest_folder
    
    # Copy the contents of the folder to the destination
    cp -r "$folder"/* "$dest_folder"
done
trial_num=$(($trial_num + 1))


echo "Last trial: $trial_num"







# Unzip all the files now
cd ./cw-ow-timing-class/data
for folder in */; do
    echo "Processing files in folder: $folder";
    cd "$folder" || continue;
    unzip -o *.zip
    cd ..;
done

