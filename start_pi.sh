#!/bin/bash
# Main script, starts application with raspberry pi camera

cd $(dirname "$0")

python3 stream.py --resolution 480 320 --fullscreen picamera
