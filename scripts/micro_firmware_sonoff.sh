#!/bin/bash

COLOR='\033[0;31m'
NC='\033[0m'
DEVICE=/dev/ttyUSB0

echo -e "${COLOR}erase flash${NC}"
read -p "Press enter to continue"
esptool.py --port "$DEVICE" erase_flash

sleep 1
echo -e "${COLOR}write esp8266-20180511-v1.9.4.bin${NC}"
read -p "Press enter to continue"
esptool.py --port "$DEVICE" write_flash -fs 1MB -fm dout 0x00000 ~/git/micropython/firmware/esp8266-20180511-v1.9.4.bin

#sleep 1
#echo -e "${COLOR}write esp_init_data_default.bin${NC}"
#read -p "Press enter to continue"
#esptool.py --port "$DEVICE" write_flash -fm dout 0x7C000 ~/git/micropython/firmware/esp_init_data_default.bin

sleep 3
echo -e "${COLOR}write webrepl_cfg.py${NC}"
read -p "Press enter to continue"
micro_usb_file.sh ~/git/micropython/sources/webrepl_cfg.py

sleep 3
echo -e "${COLOR}write boot.py${NC}"
read -p "Press enter to continue"
micro_usb_file.sh ~/git/micropython/sources/boot.py
