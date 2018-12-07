#!/bin/bash

IP=192.168.1.209

PORT=8266

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

NAME=$(basename $1)
if [[ $NAME == *.py ]] && [[ $NAME != boot.py ]] && [[ $NAME != main.py ]] && [[ $NAME != webrepl_cfg.py ]]
then
	#/home/shajen/micropython/micropython/mpy-cross/mpy-cross -O2 -mcache-lookup-bc $1
	/home/shajen/git/micropython-firmware/mpy-cross/mpy-cross -O3 $1
	FILE="${1%.py}.mpy"
else
	FILE=$1
fi

python ~/git/micropython/webrepl/webrepl_cli.py "$FILE" "$IP:$PORT:/$(basename $FILE)"
#[f if f == 'boot.py' else os.remove(f) for f in os.listdir()]
