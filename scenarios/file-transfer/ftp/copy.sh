#!/bin/bash

LOCATION=10.0.2.2
USERNAME='user'
PASSWORD='password'

ftp -in $LOCATION << SCRIPTEND
    user $USERNAME $PASSWORD
    binary
    mget rand-file
SCRIPTEND

