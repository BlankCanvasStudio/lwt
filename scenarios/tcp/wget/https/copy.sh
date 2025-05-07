#!/bin/bash

rm index*
rm ./rand-file
wget --no-check-certificate https://10.0.2.2/ > ./rand-file

