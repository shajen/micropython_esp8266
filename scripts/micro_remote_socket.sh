#!/bin/bash

DIR=$(realpath $0)
DIR=$(dirname $DIR)
FLASH_COMMAND=micro_remote_file.sh
#FLASH_COMMAND=micro_usb_file.sh

pushd "$DIR/../sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND projects/remote_socket/main.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND network/server.py
eval $FLASH_COMMAND network/pin_server_controller.py
eval $FLASH_COMMAND network/status_server_controller.py

popd
