#!/bin/bash

#esptool.py --port /dev/ttyUSB0 erase_flash
#esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/micropython/firmware/esp8266-20170108-v1.8.7.bin
#sleep 3s

#ampy --port /dev/ttyUSB0 put boot.py
#ampy --port /dev/ttyUSB0 put main.py
#ampy --port /dev/ttyUSB0 put server.py
#ampy --port /dev/ttyUSB0 put index.html
#ampy --port /dev/ttyUSB0 put webrepl_cfg.py

micropython boot.py
micropython main.py
micropython server.py
micropython index.html
micropython webrepl_cfg.py
