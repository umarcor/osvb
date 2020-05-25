from vunit import VUnit
import cocotb
from os.path import dirname
from pathlib import Path
import os

vu = VUnit.from_argv()

lib = vu.add_library("lib")
lib.add_source_files("hdl/*.vhd")

ghdl_cocotb_lib = Path(dirname(cocotb.__file__)) / 'libs' / 'libcocotbvpi_ghdl.so'
vu.set_sim_option("ghdl.sim_flags", [f"--vpi={ghdl_cocotb_lib}"])

os.environ["MODULE"] = "dff_cocotb"
os.environ["PYTHONPATH"] = "tests"

vu.main()
