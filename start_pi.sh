#!/bin/bash
# Main script, starts application with raspberry pi camera

cd $(dirname "$0")

python3 viewer.py --resolution 480 320 --fullscreen 1 --algorithm classify picamera
