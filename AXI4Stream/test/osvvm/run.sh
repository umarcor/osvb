#!/usr/bin/env bash

set -e

cd $(dirname "$0")

../../../.github/install-osvvm.sh

# TODO
# - Analyse ../../src/*.vhd
# - Analyse ./*.vhd
# - Elaborate TbStream_SendGet1
# - Simulate TbStream_SendGet1
