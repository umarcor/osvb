#!/usr/bin/env bash

set -e

$(dirname $(which ghdl))/../lib/ghdl/vendors/compile-osvvm.sh --osvvm --source $(dirname $0)/../mods/osvvm/osvvm --output precompiled
