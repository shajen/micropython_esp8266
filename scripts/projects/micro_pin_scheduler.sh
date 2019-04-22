#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
FLASH_COMMAND=$ROOT_PATH/scripts/tools/micro_remote_file.sh

pushd "${ROOT_PATH}/sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND projects/pin_scheduler/main.py
eval $FLASH_COMMAND hardware/pin_scheduler.py
eval $FLASH_COMMAND $ROOT_PATH/config
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND hardware/temperature_sensor.py
eval $FLASH_COMMAND network/mqtt_client.py
eval $FLASH_COMMAND network/status_server_controller.py

popd
