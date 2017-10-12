#!/bin/bash

#IP=192.168.0.212
IP=192.168.0.214

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

if [[ $1 == *.py ]] && [[ $1 != boot.py ]] && [[ $1 != main.py ]]
then
	#/home/shajen/micropython/micropython/mpy-cross/mpy-cross -O2 -mcache-lookup-bc $1
	#FILE="${1%.py}.mpy"
	FILE=$1
else
	FILE=$1
fi

python ~/git/micropython/webrepl/webrepl_cli.py "$FILE" "$IP:/$(basename $FILE)"
