#!/usr/bin/env sh

set -e

cd $(dirname "$0")

echo "> Analyze tb.vhd"
ghdl -a --std=08 tb.vhd

echo "> Elaborate tb"
ghdl -e --std=08 tb

echo "> Compile vpi_fpconv.c"
ghdl --vpi-compile gcc -c vpi_fpconv.c -o vpi.o

echo "> Link vpi.o"
ghdl --vpi-link gcc vpi.o -o vpi.vpi

if [ "$OS" = "Windows_NT" ]; then
  # Need to put the directory containing libghdlvpi.dll in the path.
  PATH=$PATH:`ghdl --vpi-library-dir-unix`
fi

echo "> Run tb"
ghdl -r --std=08 tb --vpi=./vpi.vpi --stop-time=1us --vcd=wave.vcd

rm *.cf
