#!/bin/bash

cd "$(dirname "$0")"
cd src

set -ex

# Measure the time taken to run go_app.py
start_time=$(date +%s)

python go_app.py

if [ $? -ne 0 ]; then
    echo "FAILURE: go_app.py failed to execute."
    exit 1
fi


end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

echo "go_app.py took $elapsed_time seconds to execute."

# Check if the execution time is more than 1 second
if [ $elapsed_time -gt 1 ]; then
    echo "FAILURE: go_app.py took longer than 1 second to execute."
    exit 1
fi


python go_science.py

if [ $? -ne 0 ]; then
    echo "FAILURE: go_science.py failed to execute."
    exit 1
fi


echo -e "\n\nSUCCESS!!\n\n"