#!/bin/bash

IP=192.168.1.209
MICROPYTHON_CROSS_COMPILER='' #if not set, upload script wtihout compilation
PORT=8266
ROOT_PATH=$(git rev-parse --show-toplevel)
PASSWORD="PASSWORD" #set the same password in webrepl_cfg.py

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

NAME=$(basename $1)

if [[ $NAME == *.py ]] && [[ $NAME != boot.py ]] && [[ $NAME != main.py ]] && [[ $NAME != webrepl_cfg.py ]] && [[ ! -z "$MICROPYTHON_CROSS_COMPILER" ]]
then
	$MICROPYTHON_CROSS_COMPILER -O2 $1
	FILE="${1%.py}.mpy"
else
	FILE=$1
fi

python $ROOT_PATH/webrepl/webrepl_cli.py -p "$PASSWORD" "$FILE" "$IP:$PORT:/$(basename $FILE)"
