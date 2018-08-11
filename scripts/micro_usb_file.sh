#!/bin/bash

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

echo $(basename $1)
ampy --baud 115200  --port /dev/ttyUSB0 put $1
