#!/bin/bash

DIR=$(realpath $0)
DIR=$(dirname $DIR)
FLASH_COMMAND=micro_remote_file.sh
#FLASH_COMMAND=micro_usb_file.sh

pushd "$DIR/../sources"

eval $FLASH_COMMAND projects/thermometer_low_power/boot.py
eval $FLASH_COMMAND projects/thermometer_low_power/main.py
eval $FLASH_COMMAND config.py
eval $FLASH_COMMAND utils.py
eval $FLASH_COMMAND network/server.py
eval $FLASH_COMMAND hardware/temperature_sensor.py
eval $FLASH_COMMAND hardware/display.py
eval $FLASH_COMMAND hardware/lcd_i2c.py
eval $FLASH_COMMAND network/status_server_controller.py

popd