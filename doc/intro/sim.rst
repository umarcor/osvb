.. _Simulators:

Simulators | Compilers
######################

.. IMPORTANT::
  Licensing constraints of many vendor tools do not allow discussing features and/or perfomance publicly. Therefore, this
  section contains references to open source tools only, which don't have such knowledge limitations.

Essent
======

*TBC*

* :ghrepo:`ucsc-vama/essent`

GHDL
====

GHDL is an open source analyzer, compiler, simulator and (experimental) synthesizer for VHDL (87, 93, 02 and 08). It has
partial support for Property Specification Language (PSL), and it can write waveforms to GHW, VCD or FST files. It supports
two co-simulation interfaces: Verilog Procedural Interface (VPI) and VHPIDIRECT (a non VHDL LRM compliant Foreign Function
Interface, which is being standardized as VFFI/VPI). GHDL can generate either executable binaries or shared libraries by
using one of three backends: GCC, LLVM or (x86_64/i386 only) mcode (built-in and in-memory ASM code generator).

* :ghrepo:`ghdl/ghdl`
* :ghrepo:`ghdl/ghdl-cosim`
* :ghrepo:`ghdl/ghdl-yosys-plugin`
* :ghrepo:`ghdl/ghdl-language-server`
* :ghrepo:`ghdl/setup-ghdl-ci`
* :ghrepo:`ghdl/extended-tests`

Icarus Verilog
==============

Icarus Verilog is an open source analyzer, compiler, simulator and (experimental) synthesizer for all of the Verilog HDL as
described in the IEEE-1364 standards. It supports Verilog Procedural Interface (VPI) for co-simulation. It is mostly used
for simulation of behavioural constructs in complex testbenches. Icarus Verilog can write waveforms to VCD, LXS2 or FST files.

* :ghrepo:`steveicarus/iverilog`
* :ghrepo:`steveicarus/ivtest`

.. _Simulators:Verilator:

Verilator
=========

Verilator is an open source analyzer and simulator for the synthesizable subsets of Verilog and SystemVerilog.
It compiles HDL sources into multithreaded C++ or SystemC, providing high-performance for large synthesizable designs.
The *verilated* model is then compiled by a C++ compiler (GCC, clang, MSVC++...), allowing generation of standalone
binaries or shared libraries, together with a user defined wrapper.
Verilator can write waveforms to VCD or FST files.
Language support is limited compared to iverilog, but it provides much faster simulation as well as implicit
obfuscation.

* :ghrepo:`verilator/verilator`
* :ghrepo:`verilator/verilator_ext_tests`
* :ghrepo:`verilator/example-systemverilog`

Although verilator does not support enough of System Verilog for using UVM yet, there is work in progress for achieving
it.
Apart from supporting System Verilog for synthesis through :awesome:`Surelog <surelog>`
and :awesome:`UHDM <uhdm>`, :web:`CHIPS Alliance <chipsalliance.org/>` members
:web:`Antmicro <antmicro.com>`, :web:`Western Digital <www.westerndigital.com/>` and :web:`Google <www.google.com/>`
are working on *verilating* non-synthesizable code, to allow running System Verilog UVM with Verilator.
See:

* :web:`Enabling open source Ibex synthesis and simulation in Verilator/Yosys via UHDM/Surelog <antmicro.com/blog/2020/12/ibex-support-in-verilator-yosys-via-uhdm-surelog/>`

* :ghrepo:`verilator/uvm <verilator/uvm>`

  * :ghrepo:`SymbiFlow/sv-tests <SymbiFlow/sv-tests>`

* :web:`Dynamic scheduling in Verilator - milestone towards open source UVM <antmicro.com/blog/2021/05/dynamic-scheduling-in-verilator>`

  * :ghrepo:`antmicro/verilator-dynamic-scheduler-examples`
  * :web:`CHIPS Alliance Deep Dive Cafe Talks Jun 15, 2021 <linuxfoundation.org/webinars/dynamic-scheduling-in-verilator-presented-by-antmicro/>`
    (
    :youtube:`Video <v=s7ivKvXGS74>`,
    :web:`Slides <chipsalliance.org/wp-content/uploads/sites/83/2021/06/Dynamic-Scheduling-in-Verilator-CHIPS-1.pdf>`
    )

Yosys/CXXRTL
============

Yosys is an open source framework for RTL synthesis tools. It has built-in Verilog 2005 support, and can process VHDL using
GHDL as a frontend (through ghdl-yosys-plugin). Yosys is written in C++ and it has a built-in simulation backed named CXXRTL.
Similarly to Verilator, CXXRTL writes out the post-synthesis netlist as a set of C++ classes. Then, a user defined wrapper
instantiates the design, toggles the clock and interacts with the ports. CXXRTL can write waveforms to VCD files. It supports
providing black boxes as behavioural C++ models, similarly to some standard co-simulation interfaces.

* :ghrepo:`YosysHQ/yosys`
* :ghrepo:`tomverbeure/cxxrtl_eval`
