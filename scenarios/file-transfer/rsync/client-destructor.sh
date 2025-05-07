#!/bin/bash
rm ./rand-file
sudo kill $(ps -e | grep rsync | awk '{print $1}')
