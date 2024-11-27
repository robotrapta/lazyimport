#!/bin/bash

cd "$(dirname "$0")"
cd src

set -ex

# Measure the time taken to run go_app.py
start_time=$(date +%s)

python go_app.py

end_time=$(date +%s)
elapsed_time=$((end_time - start_time))

echo "go_app.py took $elapsed_time seconds to execute."

# Check if the execution time is more than 1 second
if [ $elapsed_time -gt 1 ]; then
    echo "Warning: go_app.py took longer than 1 second to execute."
fi


python go_science.py