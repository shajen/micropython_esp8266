#!/bin/bash

COLOR='\033[0;31m'
NC='\033[0m'
DEVICE=/dev/ttyUSB0
ROOT_PATH=$(git rev-parse --show-toplevel)
FIRMWARE=esp8266-20180511-v1.9.4.bin

sleep 1
echo -e "${COLOR}erase flash${NC}"
read -p "Press enter to continue"
esptool.py --port "$DEVICE" erase_flash

sleep 1
echo -e "${COLOR}write $FIRMWARE${NC}"
read -p "Press enter to continue"
esptool.py --port "$DEVICE" write_flash -fs 1MB -fm dout 0x00000 "${ROOT_PATH}/firmware/$FIRMWARE"

sleep 3
echo -e "${COLOR}write webrepl_cfg.py${NC}"
read -p "Press enter to continue"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/sources/webrepl_cfg.py"

sleep 3
echo -e "${COLOR}write config${NC}"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/config"

sleep 3
echo -e "${COLOR}write boot.py${NC}"
read -p "Press enter to continue"
$ROOT_PATH/scripts/tools/micro_usb_file.sh "${ROOT_PATH}/sources/boot.py"

$ROOT_PATH/scripts/tools/micro_reboot.sh
