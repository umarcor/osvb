# This source is based on:
# 'examples/vhdl/array_axis_vcs/run.py' from VUnit (Mozilla Public License, v. 2.0)

from pathlib import Path
from vunit import VUnit
from pyCAPI import LoadCoreFile
from pyCAPI.VUnit import AddCoreFilesets

VU = VUnit.from_argv()
VU.add_random()
VU.add_verification_components()

ROOT = Path(__file__).parent

AddCoreFilesets(
    VU,
    LoadCoreFile(ROOT / '..' / '..' / "AXI4Stream.core"),
    ['common', 'test_vunit']
)

VU.main()
