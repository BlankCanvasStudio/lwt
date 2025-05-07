#!/bin/bash

filename="rand-file"
rm $filename
dd if=/dev/urandom of=$filename bs=1M count=10000

