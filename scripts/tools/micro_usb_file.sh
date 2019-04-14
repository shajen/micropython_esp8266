#!/bin/bash

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

FILE=$(basename $1)
echo $FILE

ampy --baud 115200  --port /dev/ttyUSB0 put $1 "${FILE%.py}.py"
