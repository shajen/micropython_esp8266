#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
FLASH_COMMAND=$ROOT_PATH/scripts/tools/micro_remote_file.sh

pushd "${ROOT_PATH}/sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND projects/thermostat/main.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND network/server.py
eval $FLASH_COMMAND hardware/temperature_sensor.py
eval $FLASH_COMMAND network/status_server_controller.py

popd
