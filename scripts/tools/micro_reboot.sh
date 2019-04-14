#!/bin/bash

ROOT_PATH=$(git rev-parse --show-toplevel)
source $ROOT_PATH/config
esptool.py --port $DEVICE --after hard_reset chip_id
