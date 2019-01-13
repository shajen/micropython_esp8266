#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
FLASH_COMMAND=$ROOT_PATH/scripts/tools/micro_remote_file.sh

pushd "${ROOT_PATH}/sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND projects/radar/main.py
eval $FLASH_COMMAND libraries/uPySensors/vl53l0x.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND utils.py

popd
