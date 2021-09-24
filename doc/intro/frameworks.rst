.. _OSVB:Projects:

Frameworks and Methodologies
############################

cocotb
======

Cocotb is a coroutine based co-simulation library for writing VHDL and Verilog testbenches in Python.
It was initially written and open sourced by `Potential Ventures <http://potential.ventures/cocotb>`__ in 2013.
The project went dead for some months between 2017 and 2018.
Since 2019, it is maintained by members of the `FOSSI Foundation <https://www.fossi-foundation.org/>`__ and other
contributors.

Cocotb provides shared libraries written in C++, which allows simulators to load Python scripts and interact with them
at runtime through indirect co-simulation interfaces: VPI, VHPI or FLI (see :ref:`OSVB:Co-simulation`).
Therefore, users can write testbenches for existing HDL designs using Python only.
Direct interfaces such as DPI or CXXRTL are not supported.

The provided compile and execution plumbing is based on Makefiles and environment variables.
That is loved by some users and hated by others.
There is work in progress for providing alternative build/execution workflows, without explicitly forcing users to use
an specific approach.
Using VUnit's simulator interface is one of such alternatives, which would provide a Python based solution to the most
pythonic cocotb users.

Cocotb provides logging features based on Python's ``logging`` library.
Integration of this logging approach into VUnit's Python runner is not straightforward.
Since cocotb's co-simulation scripts are loaded by the simulator in an independent instance of Python, neither VUnit nor
cocotb are explicitly aware of the other Python instance.
Moreover, different versions of Python might be used.
Anyway, simulations can be successfully executed and logs from both frameworks are usable.

There are some test management features included in cocotb.
Those allow running multiple tests with a single call/execution, instead of requiring a call for each test.
However, this feature is not as well implemented/tested as the codebase related to co-simulation.
There are different sensibilities about preserving this feature in the bundle, or removing it in favour of VUnit's
runner interface.

The list of simulators supported by cocotb is longer than the ones supported by VUnit (see :ref:`cocotb:simulator-support`
and :ref:`vunit:installing`).
The most notable difference is that cocotb supports iverilog and verilator, while the only open source simulator
supported by VUnit is GHDL.
Therefore, usage of this bundle with open source simulators is limited to VHDL designs at the moment.
Nevertheless, there is interest in evaluating again whether iverilog's improved System Verilog support can suffice for
VUnit.

* `cocotb/cocotb <https://github.com/cocotb/cocotb>`__
* `themperek/cocotb-test <https://github.com/themperek/cocotb-test>`__
* `ktbarrett/pyvertb <https://github.com/ktbarrett/pyvertb>`__

.. TIP::
  Compared to other frameworks, the cocotb ecosystem is more distributed.
  Others have most of the resources gathered in single GitHub repository.
  Conversely, there is much activity around cocotb in repositories outside of the main repository.

  * `aignacio/ravenoc: tb <https://github.com/aignacio/ravenoc/tree/master/tb>`__

.. NOTE::
  `benbr8/rstb <https://github.com/benbr8/rstb>`__ is an alternative implementation of the same approach, using Rust
  instead of Python.

OSVVM
=====

OSVVM provides an ASIC level verification methodology for VHDL that can be used on small FPGA projects.
The HDL libraries and utilities were initially provided by Jim Lewis as a learning resource in
`SynthWorks <https://synthworks.com>`__' training courses, for attendants to see the concepts applied.
In 2019 the libraries were uploaded to GitHub, and in 2020 the license was changed to Apache, since it was accepted as a
pilot program for IEEE Open Source.

The OSVVM utility library offers capabilities similar to those provided by other verification languages (such as
SystemVerilog and UVM):

* Transaction-Level Modeling
* Constrained Random test generation
* Functional Coverage with hooks for UCIS coverage database integration
* Intelligent Coverage Random test generation
* Utilities for testbench process synchronization generation
* Utilities for clock and reset generation
* Transcript files
* Error logging and reporting - Alerts and Affirmations
* Message filtering - Logs
* Scoreboards and FIFOs (data structures for verification)
* Memory models

The OSVVM model library provides the verification components for AXI4, AXI4 Lite, AXI4 Stream and UART.

The provided compile and execution plumbing is written in TCL, since it is mostly meant to be used interactively inside
the built-in shell in most vendor simulators.
Alternative installation scripts are provided by maintainers of GHDL through their
`vendor scripts <https://github.com/ghdl/ghdl/tree/master/scripts/vendors>`__.
However, those are for GHDL only, not for any simulator.

Many HDL utilities are duplicated between OSVVM and VUnit.
Nevertheless, the philosophy of both projects is different, and not necessarily conflictive.
OSVVM uses the most modern features of the language for achieving nicest looking descriptions for making advanced
features approachable.
As a result, it is on the bleeding-edge of the features that simulators do support.
Conversely, VUnit has a more conservative philosophy and tries to support the widest range of simulators, avoiding the
most recent and not broadly supported features.

Some years ago, maintainers of OSVVM and VUnit did try isolating some common HDL libraries that both projects could use
for e.g. logging features.
It didn't work back then, but there is interest in maybe trying it again in the future.
Nevertheless, having duplicated features is not an issue in the context of this bundle, since it allows each user to
pick their preferred approach.

The main stopper for using VUnit's Python features for running OSVVM's tests is that the primary unit in OSVVM's
methodology are VHDL configurations, and VUnit only supports entities as primary units.
There is common interest in hopefully extending VUnit and supporting configurations as entrypoints.

* `OSVVM/OSVVM <https://github.com/OSVVM/OSVVM>`__
* `OSVVM/OsvvmLibraries <https://github.com/OSVVM/OsvvmLibraries>`__
* `OSVVM/OSVVM-Scripts <https://github.com/OSVVM/OSVVM-Scripts>`__
* `ghdl/ghdl: scripts/vendors <https://github.com/ghdl/ghdl/tree/master/scripts/vendors>`__

  * `ghdl/extended-tests <https://github.com/ghdl/extended-tests>`__

Renode
======

Renode (developed by `Antmicro <https://www.antmicro.com/>`__) is not an HDL testing/verification framework per se.
It is presented as a development framework for accelerating IoT and embedded systems development by simulating physical
hardware systems (including the CPU, peripherals, sensors, environment and wire or wireless medium between nodes).
Precisely, in the context of IoT and embedded system, software and wire(less) communication play a crucial role in
Renode.
It allows running, debugging and testing unmodified embedded software on a workstation or laptop.

However, simulation models for custom hardware and in-development CPUs are not always available.
Moreover, it is sometimes desirable to have bit-accurate and cycle-accurate simulation models for testing custom
accelerators along with well-known CPUs and other peripherals.
As a result, there is work in progress for supporting HDL models to be added as nodes into the Renode infrastructure.
All cosimulation strategies explained in :ref:`OSVB:Co-simulation` are subject to be integrated, either using existing
Verification Components (VCs) or with ad-hoc middleware.
Find a sample about how to integrate *verilated* models in `antmicro/renode-verilator-integration <https://github.com/antmicro/renode-verilator-integration>`__.
It supports a verilated bus master and AXI4.

* `Renode <https://renode.io/>`__

  * `Using Renode for education, research and demonstration <https://antmicro.com/blog/2021/02/renode-for-education-research-and-demonstration/>`__

.. NOTE::
  `dbhi/vboard <https://github.com/dbhi/vboard>`__ includes multiple references about "*Virtual development board for
  HDL design*".
  Most of those are ad-hoc solutions, which are lacking the *project management* layer for making them plug and play.
  However, some of them implement interfaces or HDL languages which are not supported in Renode yet.

SVUnit
======

*TBC*

* `tudortimi/svunit <https://github.com/tudortimi/svunit>`__
* `dpretet/svut <https://github.com/dpretet/svut>`__

UVM
===

Universal Verification Methodology (UVM) is a standardized methodology for verifying ASIC designs.
The main implementation of UVM is available in SystemVerilog only.
Unfortunately, no open source simulator supports enough of SystemVerilog for using UVM.
At the same time, vendors don't typically support UVM in their low-end license tiers.
Therefore, although it is probably the most used methodology by ASIC designers and large companies, usage by small and
middle companies, academics, hackers and hobbyist is less significant.

Lately, several alternatives were proposed for implementing UVM in languages other than SystemVerilog.
For instance, even though iverilog cannot execute UVM in SystemVerilog, there are two projects for using UVM with
iverilog through cocotb:

* `tpoikela/uvm-python <https://github.com/tpoikela/uvm-python>`__
* `pyuvm/pyuvm <https://github.com/pyuvm/pyuvm>`__

  * `cocotb/cocotb#2418 <https://github.com/cocotb/cocotb/issues/2418>`__
  * `siemens.com/verificationhorizons: Cocotb Bus Functional Models <https://blogs.sw.siemens.com/verificationhorizons/2021/03/22/cocotb-bus-functional-models/>`__

Similarly, there is a C/C++ implementation, which uses DPI, VPI, VHPI or FLI for interacting with the RTL code:
`uvm.io <http://uvm.io/>`__.

Furthermore, there work in progress for adding System Verilog support to verilator, including both synthesizable and
non-synthesizable constructs. See :ref:`OSVB:Simulators:Verilator`.

UVVM
====

*TBC*

* `UVVM <https://github.com/UVVM/UVVM>`__

VUnit
=====

VUnit is an open source unit testing framework for VHDL/SystemVerilog.
It was developed and maintained by Lars Asplund and Olof Kraigher and it was initially released in 2015.
Several users contributed and maintain verification components.
Unai Martinez-Corral contributed co-simulation features to be used with GHDL's implementation of VHPIDIRECT (see
:ref:`OSVB:Co-simulation`).

The main focus of VUnit is providing the functionality needed to realize continuous and automated testing of HDL code.
It provides a Python API for declaring sources and library names, for parameterizing tests and for defining simulator
execution parameters.
The simulator interface is coupled with a test runner implemented both in Python and in HDL.
That allows hardware designers to define tests in HDL, thus, complementing traditional HDL only testing methodologies.
It brings multiple concepts for Test Driven Design (TDD) from software into the hardware design.

Optional HDL libraries include utilities for checks, logging, handling arrays, randomization, etc. as well as a
communication package for modelling abstract messaging channels.
Verification components for several standard interfaces are provided based on the communication package.
Custom types are also provided for allowing dynamic allocation of pointers (accesses).

VUnit includes the core of OSVVM as a submodule.
It also includes `JSON-for-VHDL <https://github.com/Paebbels/JSON-for-VHDL>`_, which allows passing arbitrarily complex
generics to the testbenches, by providing them as encoded JSON strings.

Using the OSVVM Libraries and UVVM with VUnit is possible but not straightforward.
In VUnit, libraries and sources are declared in a Python script, using VUnit's API.
Users have three options:

* Manually declaring which sources belong to each library, in the Python run script.
* Using the TCL scripts provided by OSVVM/UVVM for pre-compiling the frameworks, and then provide the locations to the
  pre-built sources in the Python script.
* Using GHDL's vendor scripts for pre-compiling the frameworks, and then provide the locations by passing
  :option:`-P <ghdl.-P>` to GHDL in the Python script.

None of them is ideal.
The first one requires all users to repeat some code which might be easily reused.
Others require dealing with paths/locations specific to each host/system.
Instead, the approach in this bundle uses ``*.core`` files and :ref:`OSVB:API:Core`.

With regard to simulator support, VUnit does currently not support any open source Verilog or System Verilog simulator.
However, it was last evaluated 3-4 years ago (see `VUnit/vunit#188 <https://github.com/VUnit/vunit/issues/188>`__).
Since both iverilog and iverilog were improved, and specially System Verilog support, it might be possible to use them
with VUnit nowadays.

* `VUnit/vunit <https://github.com/VUnit/vunit>`__
* `VUnit/vunit_action <https://github.com/VUnit/vunit_action>`__
* `VUnit/tdd-intro <https://github.com/VUnit/tdd-intro>`__
* `VUnit/cosim <https://github.com/VUnit/cosim>`__

.. NOTE::
  `Malcolmnixon/VhdlTest <https://github.com/Malcolmnixon/VhdlTest>`__ is a proof of concept of a minimal implementation
  of the Python runner in VUnit.
  It's for VHDL testbenches only, and supports GHDL or Active-HDL.
  It requires a YAML configuration file for specifying the project, instead of using a Python script.
  This feature is related to :ref:`OSVB:API:Core`.

Learning/teaching
=================

* `Course content for the Design Verification module at the University of Bristol <https://uobdv.github.io/Design-Verification/>`__
* `umarcor: references/VHDL.bib <https://github.com/umarcor/umarcor/blob/main/references/VHDL.bib>`__
