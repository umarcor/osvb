#!/usr/bin/env sh

# Authors:
#   Unai Martinez-Corral
#
# Copyright 2020-2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

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
