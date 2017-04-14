#!/bin/bash

DIR=$(realpath $0)
DIR=$(dirname $DIR)
FLASH_COMMAND=micro_remote_file.sh
#FLASH_COMMAND=micro_usb_file.sh

pushd "$DIR/../sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND main.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND helper.py
eval $FLASH_COMMAND devices.py
eval $FLASH_COMMAND display.py
eval $FLASH_COMMAND lcd_i2c.py

popd
