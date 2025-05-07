#!/bin/bash

source ./config-test.sh

FILENAMES=()

while [[ $# -gt 0 ]]; do
    FILENAMES+=("$1")
    shift
done

# If there are no filenames specified, used config
if [ ${#FILENAMES[@]} -eq 0 ]; then
    FILENAMES+=("$expr_name")
fi

for name in "${FILENAMES[@]}"; do
    cd $data_dir/$name
    unzip *.zip
    cd ../..
done

