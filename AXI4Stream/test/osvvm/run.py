# This source is based on:
# 'examples/vhdl/array_axis_vcs/run.py' from VUnit (Mozilla Public License, v. 2.0)

from pathlib import Path
from vunit import VUnit

VU = VUnit.from_argv()
VU.add_verification_components()

ROOT = Path(__file__).parent

VU.add_library("lib").add_source_files([
    ROOT / "*.vhd",
    ROOT / '..' / '..' / "src" / "*.vhd"
])

VU.main()
