.. _OSVB:Examples:AXI4Stream:

SISO AXI4 Stream
################

The purpose of this example is showcasing a testing setup for a core with Single Input Single Output (SISO) AXI4 Stream
interfaces. This is typically found in streaming Digital Signal Processing (DSP) applications. For illustration purposes,
the same UUT is tested using verification components and run scripts from several frameworks.

:ghsrc:`AXI4Stream/src <AXI4Stream/src>` contains the VHDL sources of a SISO AXI4 Stream loopback buffer. Those sources are
the same as the ones in the `array_axis_vcs <https://github.com/VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs>`__
example of VUnit's repo.

VUnit's array_axis_vcs example
==============================

:ghsrc:`AXI4Stream/test/vunit/*.vhd <AXI4Stream/test/vunit/*.vhd>` are regular VUnit testbenches, similar to the ones found in
`VUnit/vunit: examples/vhdl/array_axis_vcs <https://github.com/VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs>`__.
However, several variants were added here, for testing performance with different setups.

Regular VUnit run script
------------------------

:ghsrc:`AXI4Stream/test/vunit/run.py <AXI4Stream/test/vunit/run.py>` is a regular VUnit script, similar to the one found in
`VUnit/vunit: examples/vhdl/array_axis_vcs/run.py <https://github.com/VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs/run.py>`__.
It searches the testbenches in the same directory, and executes the tests as usual in a VUnit run.

VUnit run script with pyCAPI
----------------------------

:ghsrc:`AXI4Stream/test/vunit/run_capi.py <AXI4Stream/test/vunit/run_capi.py>` is a variant of the default script, which uses
:ref:`OSVB:pyCAPI` for retrieving the filesets. Testbenches are found and executed as usual.

OSVVM TBStream
==============

:ghsrc:`AXI4Stream/test/osvvm <AXI4Stream/test/osvvm>` contains VHDL sources based on OSVVM's AXI4 Stream testbench example:
`OSVVM/AXI4: AxiStream/testbench <https://github.com/OSVVM/AXI4/tree/master/AxiStream/testbench>`__.

OSVVM build and test scripts
----------------------------

*TBC*

GHDL's vendor build scripts and OSVVM's test scripts
----------------------------------------------------

*TBC*

GHDL's vendor build scripts and VUnit
-------------------------------------

*TBC*

OSVVM's build scripts and VUnit
-------------------------------

*TBC*

VUnit with pyCAPI
-----------------

*TBC*

.. HINT::
  Probably, use GHDL's `compile-osvvm.ps1 <https://github.com/ghdl/ghdl/blob/master/scripts/vendors/compile-osvvm.ps1>`__ for
  generating ``*.core`` files automatically.
