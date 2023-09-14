#!/usr/bin/env bash

cd $(dirname "$0")

pip3 install -r ../mods/pyOSVDE/requirements.txt

git clone https://github.com/antmicro/fpga-topwrap
pip3 install -r fpga-topwrap/requirements.txt

git clone https://github.com/stnolting/neorv32
cp neorv32.osvdeignore neorv32/.osvdeignore

./main.py ./neorv32
