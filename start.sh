#!/bin/bash
# Main script, starts application with webcam

cd $(dirname "$0")

python3 stream.py --resolution 600 400 --location 1 webcam
#python3 stream.py -l files/test.jpg image
