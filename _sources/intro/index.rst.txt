.. _OSVB:Overview:

Overview
========

The block diagram below illustrates how the components fit together in this bundle:

.. figure:: ../_static/osvb.png
  :alt: Block diagram of the OSVB
  :width: 100%
  :align: center

  Block diagram of the Open Source Verification Bundle.

The language of choice for integration is Python.
Some verification projects do use Python already; others provide scripts written in TCL, Perl or Bash.
However, the wider open source ecosystem for hardware design is dominated by Python.
It's the fastest growing language in many fields, and specially in the embedded world.

Among the frameworks providing a Python based simulator interface and test management plumbing, VUnit's solution is the
most mature and feature complete.
It does also provide a neat integration between Python and top-level testbenches, allowing hardware designers to define
multiple test cases in HDL, but have them handled from Python.
Therefore, the core of OSVB are VUnit's Python modules.

cocotb's main feature is providing shared libraries for allowing co-simulation from Python.
Moreover, the Python modules for co-simulation are loaded by the simulator, not by the caller.
Therefore, any simulator interface and task management plumbing for regular HDL designs is suitable for executing
testbenches with cocotb's co-simulation features.
That is the case with VUnit.
However, there is a conflict with the test management features in both frameworks.
Both of them expect to be the root of the management, thus they both finalise individual test/simulations independently.
There is a race between them, and one will always fail.
There is work in progress for letting one of them wait for the other.
See :ref:`OSVB:Examples:SFF:VUnit-cocotb`.

OSVVM is composed by a core repository and a larger distribution named *OSVVM Libraries*, which includes verification
components and build/run scripts.
VUnit does include the core as a built-in feature, since randomisation features are based on that.
However, other libraries are not included by default.
The missing repositories might be added as built-in VUnit modules too, but it increases the maintenance burden of VUnit
and it's not an scalable approach.
OSVVM does provide ``*.pro`` files, which uses a custom syntax for defining sources and the compilation order.
Those files are used by OSVVM's own TCL scripts and also by `GHDL's vendor scripts <https://github.com/ghdl/ghdl/tree/master/scripts/vendors>`__ (written in PowerShell and Bash).
Yet, writing a custom Python module for reading those files doesn't feel worth.
Instead, the proposal in this bundle is to use ``*.core`` (YAML) files.
See :ref:`OSVB:API:Core`.
Furthermore, the entrypoint to tests based on the OSVVM methodology are VHDL configurations, unlike other methodologies
based on entities.
Currently, VUnit's runner does not support executing configurations as primary units.
However, there is common interest in making it possible.

Similarly, UVVM is not supported as a built-in feature in VUnit, but ``compile_order.txt`` files are provided.
Those are used by UVVM's own TCL scripts and also by GHDL's vendor scripts (written in PowerShell and Bash).
As with OSVVM, the proposal in this bundle is to use ``*.core`` (YAML) files. See :ref:`OSVB:API:Core`.

While VUnit provides multiple optional helper VHDL libraries, the SystemVerilog infrastructure is limited to the HDL
runner and some `check` features.
Conversely, SVUnit is for SystemVerilog mostly.
The test management features in SVUnit are implemented using Perl, and installation scripts are written in bash/csh.
As a result, it would be interesting to handle SVUnit's HDL resources through VUnit's simulator interface and runner.
There is no work in progress in this regard yet.

Since this bundle is focused on simulation of HDL-centric testbenches, synthesis and formal verification are out of the
scope.
However, most projects are to be implemented in practice, and the sources of Units Under Test (UUTs) are to be used for
both simulation and implementation.
Therefore, the usage of :ref:`OSVB:API:Core` in this bundle is not limited to adding verification frameworks
and/or methodologies; it is also the proposed solution for users to declare the sources of their designs.
By the same token, :ref:`OSVB:API:Project`, :ref:`OSVB:API:Tool`, :ref:`OSVB:API:Runner` and :ref:`OSVB:API:Logging` are
also extensible for being used in synthesis and implementation.
