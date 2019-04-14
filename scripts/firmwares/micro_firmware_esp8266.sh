#!/bin/bash

COLOR='\033[0;31m'
NC='\033[0m'
ROOT_PATH=$(git rev-parse --show-toplevel)
FIRMWARE=esp8266-20190125-v1.10.bin
INIT_DATA=esp_init_data_default.bin
source $ROOT_PATH/config

sleep 1
echo -e "${COLOR}erase flash${NC}"
esptool.py --port "$DEVICE" erase_flash

sleep 1
echo -e "${COLOR}write $FIRMWARE${NC}"
esptool.py --port "$DEVICE" write_flash -fm dio 0x00000 "${ROOT_PATH}/firmware/$FIRMWARE"

sleep 1
echo -e "${COLOR}write $INIT_DATA${NC}"
esptool.py --port "$DEVICE" write_flash 0x3fc000 "${ROOT_PATH}/firmware/$INIT_DATA"

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
