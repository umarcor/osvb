#!/usr/bin/env python3

from pathlib import Path
from vunit import VUnit
from vunit_osvvm import add_osvvmlibs


ROOT = Path(__file__).parent


VU = VUnit.from_argv()

# Non-builtin OSVVMLibraries are added through a helper package.
# The version of OSVVMLibraries needs to be compatible with the builtin OSVVM version.
add_osvvmlibs(
    VU,
    Sources=ROOT / "../../../mods/osvvm",
    NoCore=True,
    Version="2021.09"
)

# VUnit's Verification Components are added after non-builtin content.
# Since previously added content did not include a library named OSVVM,
# the builtin version is compiled (which is a dependency of add_verification_components).
VU.add_verification_components()

VU.add_library("lib").add_source_files([ROOT / "*.vhd", ROOT / ".." / ".." / "src" / "*.vhd"])

VU.main()
