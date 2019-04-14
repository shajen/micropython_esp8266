#!/bin/bash

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

ROOT_PATH=$(git rev-parse --show-toplevel)
source $ROOT_PATH/config

FILE=$(basename $1)
echo $FILE

ampy --baud 115200  --port $DEVICE put $1 "${FILE%.py}.py"
