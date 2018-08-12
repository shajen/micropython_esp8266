#!/bin/bash

COLOR='\033[0;31m'
NC='\033[0m'
DEVICE=/dev/ttyUSB0

echo -e "${COLOR}erase flash${NC}"
esptool.py --port "$DEVICE" erase_flash

sleep 1
echo -e "${COLOR}write esp8266-20180511-v1.9.4.bin${NC}"
esptool.py --port "$DEVICE" write_flash -fm dio 0x00000 ~/git/micropython/firmware/esp8266-20180511-v1.9.4.bin
sleep 1
echo -e "${COLOR}write esp_init_data_default.bin${NC}"
esptool.py --port "$DEVICE" write_flash 0x3fc000 ~/git/micropython/firmware/esp_init_data_default.bin

sleep 3
echo -e "${COLOR}write boot.py${NC}"
micro_usb_file.sh ~/git/micropython/sources/boot.py

#esptool.py --port /dev/ttyUSB0 read_flash 0x3fc000 128 ~/git/micropython/firmware/esp_init_data_default.bin

micro_reboot.sh
