#!/bin/bash
# Main script, starts application

cd $(dirname "$0")

python3 ./stream.py 480 320
