#!/usr/bin/env python3

from pathlib import Path
from vunit import VUnit
from vunit_osvvm import add_osvvmlibs


ROOT = Path(__file__).parent


VU = VUnit.from_argv()

# Any version OSVVM and OSVVMLibraries can be added through a helper package.
# It does not need to match the version of the OSVVM submoduled in VUnit,
# but it needs to be compatible with the features used by VUnit's builtins.
add_osvvmlibs(
    VU,
    Sources=ROOT / "../../../mods/osvvm"
)

# VUnit's Verification Components are added after non-builtin content was added, including a library named OSVVM.
# The builtin add_osvvm is skipped, despite it being a dependency of add_verification_components.
# TODO: in fact, VUnit crashes at the moment because the skipping functionality was not implemented yet:
# https://github.com/VUnit/vunit/issues/767
VU.add_verification_components()

VU.add_library("lib").add_source_files([ROOT / "*.vhd", ROOT / ".." / ".." / "src" / "*.vhd"])

VU.main()
