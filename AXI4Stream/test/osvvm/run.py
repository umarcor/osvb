# This source is based on:
# 'examples/vhdl/array_axis_vcs/run.py' from VUnit (Mozilla Public License, v. 2.0)

from pathlib import Path
from vunit import VUnit


# Can't compile all OSVVM files since some depends on simulator
# This naive filter compiles everything except Aldec and Cadence related files
def osvvm_filter_files(path):
    return [
        file
        for file in path.glob("*.vhd")
        if (not str(file).endswith("_c.vhd") and not str(file).endswith("_Aldec.vhd"))
    ]


ROOT = Path(__file__).parent
OSVVM = ROOT / "../../../mods/osvvm"

VU = VUnit.from_argv()

VU.add_library("OSVVM").add_source_files(osvvm_filter_files(OSVVM / "osvvm"))
VU.add_library("OSVVM_Common").add_source_files(OSVVM / "Common/src/*.vhd")
VU.add_library("OSVVM_AXI4").add_source_files(
    [OSVVM / f"AXI4/{subdir}/src/*.vhd" for subdir in ["common", "AxiStream", "Axi4"]]
)

VU.add_library("lib").add_source_files([ROOT / "*.vhd", ROOT / ".." / ".." / "src" / "*.vhd"])

VU.main()
