#!/bin/bash

COLOR='\033[0;31m'
NC='\033[0m'
ROOT_PATH=$(git rev-parse --show-toplevel)
FIRMWARE=esp32-20190125-v1.10.bin
source $ROOT_PATH/config

sleep 1
echo -e "${COLOR}erase flash${NC}"
esptool.py --port "$DEVICE" erase_flash

sleep 1
echo -e "${COLOR}write $FIRMWARE${NC}"
esptool.py --port "$DEVICE" write_flash -fm dio 0x1000 "${ROOT_PATH}/firmware/$FIRMWARE"

sleep 3
echo -e "${COLOR}write webrepl_cfg.py${NC}"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/sources/webrepl_cfg.py"

sleep 3
echo -e "${COLOR}write config${NC}"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/config"

sleep 3
echo -e "${COLOR}write boot.py${NC}"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/sources/boot.py"

$ROOT_PATH/scripts/tools/micro_reboot.sh

# TODO: auto run on esp32 this command:
# import upip
# upip.install('micropython-uasyncio')
