#!/usr/bin/env sh

set -e

cd $(dirname "$0")

echo "> Analyze tb.vhd"
ghdl -a --time-resolution=auto ent.vhd tb.vhd

echo "> Elaborate tb"
ghdl -e tb

echo " > Run tb"
ghdl -r --time-resolution=auto tb --stop-time=1us --vcd=wave.vcd

rm *.cf
