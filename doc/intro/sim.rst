.. _OSVB:Simulators:

Simulators | Compilers
######################

.. IMPORTANT::
  Licensing constraints of many vendor tools do not allow discussing features and/or perfomance publicly. Therefore, this
  section contains references to open source tools only, which don't have such knowledge limitations.

Essent
======

*TBC*

* `ucsc-vama/essent <https://github.com/ucsc-vama/essent>`__

GHDL
====

GHDL is an open source analyzer, compiler, simulator and (experimental) synthesizer for VHDL (87, 93, 02 and 08). It has
partial support for Property Specification Language (PSL), and it can write waveforms to GHW, VCD or FST files. It supports
two co-simulation interfaces: Verilog Procedural Interface (VPI) and VHPIDIRECT (a non VHDL LRM compliant Foreign Function
Interface, which is being standardized as VFFI/VPI). GHDL can generate either executable binaries or shared libraries by
using one of three backends: GCC, LLVM or (x86_64/i386 only) mcode (built-in and in-memory ASM code generator).

* `ghdl/ghdl <https://github.com/ghdl/ghdl>`__
* `ghdl/ghdl-cosim <https://github.com/ghdl/ghdl-cosim>`__
* `ghdl/ghdl-yosys-plugin <https://github.com/ghdl/ghdl-yosys-plugin>`__
* `ghdl/ghdl-language-server <https://github.com/ghdl/ghdl-language-server>`__
* `ghdl/setup-ghdl-ci <https://github.com/ghdl/setup-ghdl-ci>`__
* `ghdl/extended-tests <https://github.com/ghdl/extended-tests>`__

Icarus Verilog
==============

Icarus Verilog is an open source analyzer, compiler, simulator and (experimental) synthesizer for all of the Verilog HDL as
described in the IEEE-1364 standards. It supports Verilog Procedural Interface (VPI) for co-simulation. It is mostly used
for simulation of behavioural constructs in complex testbenches. Icarus Verilog can write waveforms to VCD, LXS2 or FST files.

* `steveicarus/iverilog <https://github.com/steveicarus/iverilog>`__
* `steveicarus/ivtest <https://github.com/steveicarus/ivtest>`__

.. _OSVB:Simulators:Verilator:

Verilator
=========

Verilator is an open source analyzer and simulator for the synthesizable subsets of Verilog and SystemVerilog.
It compiles HDL sources into multithreaded C++ or SystemC, providing high-performance for large synthesizable designs.
The *verilated* model is then compiled by a C++ compiler (GCC, clang, MSVC++...), allowing generation of standalone
binaries or shared libraries, together with a user defined wrapper.
Verilator can write waveforms to VCD or FST files.
Language support is limited compared to iverilog, but it provides much faster simulation as well as implicit
obfuscation.

* `verilator/verilator <https://github.com/verilator/verilator>`__
* `verilator/verilator_ext_tests <https://github.com/verilator/verilator_ext_tests>`__
* `verilator/example-systemverilog <https://github.com/verilator/example-systemverilog>`__

Although verilator does not support enough of System Verilog for using UVM yet, there is work in progress for achieving
it.
Apart from supporting System Verilog for synthesis through `Surelog <https://hdl.github.io/awesome/items/surelog/>`__
and `UHDM <https://hdl.github.io/awesome/items/uhdm/>`__, `CHIPS Alliance <https://chipsalliance.org/>`__ members
`Antmicro <https://antmicro.com>`__, `Western Digital <https://www.westerndigital.com/>`__ and `Google <https://www.google.com/>`__
are working on *verilating* non-synthesizable code, to allow running System Verilog UVM with Verilator.
See:

* `Enabling open source Ibex synthesis and simulation in Verilator/Yosys via UHDM/Surelog <https://antmicro.com/blog/2020/12/ibex-support-in-verilator-yosys-via-uhdm-surelog/>`__

* `verilator/uvm <https://github.com/verilator/uvm>`__

  * `SymbiFlow/sv-tests <https://github.com/SymbiFlow/sv-tests>`__

* `Dynamic scheduling in Verilator - milestone towards open source UVM <https://antmicro.com/blog/2021/05/dynamic-scheduling-in-verilator/>`__

  * `antmicro/verilator-dynamic-scheduler-examples <https://github.com/antmicro/verilator-dynamic-scheduler-examples>`__
  * `CHIPS Alliance Deep Dive Cafe Talks Jun 15, 2021 <https://linuxfoundation.org/webinars/dynamic-scheduling-in-verilator-presented-by-antmicro/>`__
    (
    `Video <https://www.youtube.com/watch?v=s7ivKvXGS74>`__,
    `Slides <https://chipsalliance.org/wp-content/uploads/sites/83/2021/06/Dynamic-Scheduling-in-Verilator-CHIPS-1.pdf>`__
    )

Yosys/CXXRTL
============

Yosys is an open source framework for RTL synthesis tools. It has built-in Verilog 2005 support, and can process VHDL using
GHDL as a frontend (through ghdl-yosys-plugin). Yosys is written in C++ and it has a built-in simulation backed named CXXRTL.
Similarly to Verilator, CXXRTL writes out the post-synthesis netlist as a set of C++ classes. Then, a user defined wrapper
instantiates the design, toggles the clock and interacts with the ports. CXXRTL can write waveforms to VCD files. It supports
providing black boxes as behavioural C++ models, similarly to some standard co-simulation interfaces.

* `YosysHQ/yosys <https://github.com/YosysHQ/yosys>`__
* `tomverbeure/cxxrtl_eval <https://github.com/tomverbeure/cxxrtl_eval>`__
