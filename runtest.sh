#!/bin/bash

cd "$(dirname "$0")"
cd src

set -ex

python app/go.py
