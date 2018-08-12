#!/bin/bash

DIR=$(realpath $0)
DIR=$(dirname $DIR)
FLASH_COMMAND=micro_remote_file.sh
#FLASH_COMMAND=micro_usb_file.sh

pushd "$DIR/../sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND water_can/main.py
eval $FLASH_COMMAND water_can/water_can_controller.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND devices.py
eval $FLASH_COMMAND server.py
eval $FLASH_COMMAND status_server_controller.py

popd
