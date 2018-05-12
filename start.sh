#!/bin/bash
# Main script, starts application with webcam

cd $(dirname "$0")

python3 viewer.py --resolution 600 400 --location 0 --algorithm classify webcam
#python3 viewer.py -l files/test.jpg image
