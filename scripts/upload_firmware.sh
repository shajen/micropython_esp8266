#!/bin/bash

esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/micropython/firmware/esp8266-20170108-v1.8.7.bin

sleep 1
ampy --baud 115200 --port /dev/ttyUSB0 put boot.py
sleep 1
ampy --baud 115200 --port /dev/ttyUSB0 put webrepl_cfg.py
