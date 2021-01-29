import os
from pathlib import Path

from vunit import VUnit
import cocotb


ROOT = Path(__file__).parent.resolve()

VU = VUnit.from_argv()

LIB = VU.add_library("lib")
LIB.add_source_files([
    ROOT.parent / "src" / "*.vhd",
    ROOT / "*.vhd"
])

def pre_cfg():
    os.environ["MODULE"] = "dff_cocotb"
    os.environ["PYTHONPATH"] += ":%s" % str(ROOT)
    return True

for testbench in LIB.get_test_benches("*tb_dff*"):
    for test in testbench.get_tests():
        if test.name == "cocotb":
            test.set_sim_option("ghdl.sim_flags", ["--vpi=%s" %
                str(Path(cocotb.__file__).parent.resolve() / 'libs' / 'libcocotbvpi_ghdl.so')
            ])
            test.set_pre_config(pre_cfg)

VU.main()
