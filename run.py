import os
from pathlib import Path

from vunit import VUnit
import cocotb


VU = VUnit.from_argv()

VU.add_library("lib").add_source_files("*.vhd")

VU.set_sim_option("ghdl.sim_flags", ["--vpi=%s" %
    str(Path(cocotb.__file__).parent.resolve() / 'libs' / 'libcocotbvpi_ghdl.so')
])

os.environ["MODULE"] = "dff_cocotb"
os.environ["PYTHONPATH"] = "tests"

VU.main()
