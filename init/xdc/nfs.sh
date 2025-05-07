#!/bin/bash

ansible-playbook -vvv -i init/resources/inventory.ini init/resources/mount-lighthouse-nfs.yml

