#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
FLASH_COMMAND=$ROOT_PATH/scripts/tools/micro_remote_file.sh

pushd "${ROOT_PATH}/sources"

eval $FLASH_COMMAND boot.py
eval $FLASH_COMMAND projects/ws2812/main.py
eval $FLASH_COMMAND projects/ws2812/pre_boot.py
eval $FLASH_COMMAND $ROOT_PATH/config
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND network/mqtt_client.py
eval $FLASH_COMMAND network/status_server_controller.py
eval $FLASH_COMMAND network/ws2812_server_controller.py
eval $FLASH_COMMAND ws2812/animation_utils.py
eval $FLASH_COMMAND ws2812/strip_animation.py
eval $FLASH_COMMAND ws2812/full_smooth_transition_animation.py
eval $FLASH_COMMAND ws2812/rainbow_animation.py

popd
