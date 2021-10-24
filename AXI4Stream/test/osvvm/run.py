#!/usr/bin/env python3

from pathlib import Path
from vunit import VUnit
from vunit_osvvm import add_osvvmlibs


ROOT = Path(__file__).parent


VU = VUnit.from_argv()

# Since all of OSVVM and OSVVMLibraries are added below, potentially conflictive VUnit builtins are avoided in this script:
# NO add_osvvm
# NO add_random
# NO add_verification_components

# Any version OSVVM and OSVVMLibraries can be added through a helper package.
add_osvvmlibs(
    VU,
    Sources=ROOT / "../../../mods/osvvm"
)

VU.add_library("lib").add_source_files([ROOT / "*.vhd", ROOT / ".." / ".." / "src" / "*.vhd"])

VU.main()
