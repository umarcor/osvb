#!/usr/bin/env bash

set -e

OSVVM="$(dirname "$0")/../mods/osvvm/osvvm"

# Temporarily revert OSVVM to 2021.06
# https://github.com/ghdl/ghdl/issues/1900
cd "$OSVVM"/..
git checkout -b v2021.06 2021.06
git submodule update --init --recursive
cd -

# Currently, the bash variant of GHDL's vendor scripts supports the core of OSVVM only
$(dirname $(which ghdl))/../lib/ghdl/vendors/compile-osvvm.sh --all --source "$OSVVM" --output precompiled
