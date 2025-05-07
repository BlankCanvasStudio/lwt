#!/bin/bash
sudo kill $(ps -e | grep ping | awk '{print $1}')
