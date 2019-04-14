#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
source $ROOT_PATH/config

[[ -z "$1" ]] && echo "File $1 not found." && exit 0

NAME=$(basename $1)
SRC_FILE=$1
DST_FILE=$NAME

if [[ $NAME == *.py ]] && [[ $NAME != boot.py ]] && [[ $NAME != main.py ]] && [[ $NAME != webrepl_cfg.py ]] && [[ ! -z "$MICROPYTHON_CROSS_COMPILER" ]]
then
	$MICROPYTHON_CROSS_COMPILER -O2 $1
	SRC_FILE="${1%.py}.mpy"
	DST_FILE="${NAME%.py}.mpy"
elif [[ $NAME == config ]]
then
	DST_FILE="${NAME%.py}.py"
fi

python $ROOT_PATH/webrepl/webrepl_cli.py -p "$PASS" "$SRC_FILE" "$IP:$PORT:/$(basename $DST_FILE)"
