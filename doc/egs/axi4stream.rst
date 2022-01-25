.. _Examples:AXI4Stream:

SISO AXI4 Stream
################

The purpose of this example is to showcase a testing setup for a core with Single Input Single Output (SISO) AXI4 Stream
interfaces.
This is typically found in streaming Digital Signal Processing (DSP) applications.
For illustration purposes, the same UUT is tested using verification components and run scripts from several frameworks.

:ghsrc:`AXI4Stream/src <AXI4Stream/src>` contains the VHDL sources of a SISO AXI4 Stream loopback buffer.
Those sources are the same as the ones in the :ghrepo:`array_axis_vcs <VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs>`
example of VUnit's repo.

VUnit's array_axis_vcs example
******************************

:ghsrc:`AXI4Stream/test/vunit/*.vhd <AXI4Stream/test/vunit/>` are regular VUnit testbenches using VUnit's
Verification Components (VCs), similar to the ones found in :ghrepo:`VUnit/vunit: examples/vhdl/array_axis_vcs <VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs>`.
However, several variants were added here, for testing performance with different setups.

VUnit
=====

:ghsrc:`AXI4Stream/test/vunit/run.py <AXI4Stream/test/vunit/run.py>` is a regular VUnit script based on
:ghrepo:`VUnit/vunit: examples/vhdl/array_axis_vcs/run.py <VUnit/vunit/tree/master/examples/vhdl/array_axis_vcs/run.py>`.
It searches the testbenches in the same directory, and executes the tests as usual in a VUnit run.

This is ``test_AXI4Stream_VUnit`` in CI.

With pyCAPI
-----------

:ghsrc:`AXI4Stream/test/vunit/run_capi.py <AXI4Stream/test/vunit/run_capi.py>` is a variant of the default script, which
uses :ref:`API:Core` for retrieving the filesets.
Testbenches are found and executed as usual.

This is ``test_AXI4Stream_VUnitCAPI`` in CI.

OSVVM TBStream
**************

:ghsrc:`AXI4Stream/test/osvvm <AXI4Stream/test/osvvm>` contains VHDL sources based on OSVVM's AXI4 Stream testbench
example: :ghrepo:`OSVVM/AXI4: AxiStream <OSVVM/AXI4/tree/master/AxiStream>`.

OSVVM ``.pro`` files
====================

OSVVM provides a compilation and execution infrastructure through files with extension ``.pro``, which are in fact TCL
scripts.
Those scripts are used in the CI workflow of :ghrepo:`osvvm/OsvvmLibraries <osvvm/OsvvmLibraries>`.

:ghsrc:`AXI4Stream/test/osvvm/run.pro <AXI4Stream/test/osvvm/run.pro>` sources OSVVM's scripts and uses the ``analyze``
``simulate`` commands provided by those.

This is ``test_AXI4Stream_OSVVM_ProFiles`` in CI.

GHDL's vendor scripts
=====================

Maintainers of GHDL provide helper scripts to build vendor libraries, including Xilinx, Intel/Altera,... and OSVVM
(see :ghrepo:`ghdl/ghdl: scripts/vendors <ghdl/ghdl/tree/master/scripts/vendors>`).
Currently, Bash and PowerShell variants of the scripts are provided.
Those scripts are used in the CI workflow of :ghrepo:`ghdl/extended-tests`.

.. HINT::
  GHDL's vendor scripts are typically used along with custom simulation scripts or with VUnit.
  Is it possible to use them for compilation and OSVVM's ``.pro`` files for running the simulations?

VUnit
=====

Since VUnit allows managing the compilation of VHDL sources or adding externally built libraries, there are multiple
possibilities for combining the OSVVM methodology and the VUnit framework.
Ten different use cases are showcased in this repository, nine of which are summarised in the following table:

========================  ==========================================================  ==========================================================================  ============================================================================
Order \\ Build procedure  RunScript                                                   ProFiles                                                                    VendorScripts
========================  ==========================================================  ==========================================================================  ============================================================================
Without VUnit's VCs       :ghsrc:`run.py <AXI4Stream/test/osvvm/run.py>`              :ghsrc:`run_ext_pro.py <AXI4Stream/test/osvvm/run_ext_pro.py>`              :ghsrc:`run_ext_ghdl.py <AXI4Stream/test/osvvm/run_ext_ghdl.py>`
With VUnit's VCs Before   :ghsrc:`run_wvcsb.py <AXI4Stream/test/osvvm/run_wvcsb.py>`  :ghsrc:`run_ext_pro_wvcsb.py <AXI4Stream/test/osvvm/run_ext_pro_wvcsb.py>`  :ghsrc:`run_ext_ghdl_wvcsb.py <AXI4Stream/test/osvvm/run_ext_ghdl_wvcsb.py>`
With VUnit's VCs After    :ghsrc:`run_wvcsa.py <AXI4Stream/test/osvvm/run_wvcsa.py>`  :ghsrc:`run_ext_pro_wvcsa.py <AXI4Stream/test/osvvm/run_ext_pro_wvcsa.py>`  :ghsrc:`run_ext_ghdl_wvcsa.py <AXI4Stream/test/osvvm/run_ext_ghdl_wvcsa.py>`
========================  ==========================================================  ==========================================================================  ============================================================================

where:

* ``RunScript``: compiling sources through VUnit.
* ``ProFiles``: using OSVVM's ``.pro`` files for building OSVVMLibraries, and then adding them as external to VUnit.
* ``VendorScripts``: using GHDL's vendor scripts for building OSVVMLibraries, and then adding them as external to
  VUnit.

and:

* ``Before``: VUnit's ``add_verification_components`` (including the builtin OSVVM) is used before adding non-builtin
  OSVVMLibraries.
* ``After``: non-builtin OSVVM and/or OSVVMLibraries are added before using VUnit's ``add_verification_components``.

Moreover, :ghsrc:`run_wvcsans.py <AXI4Stream/test/osvvm/run_wvcsans.py>` is equivalent to ``run_wvcsb.py``, but the
resources are added in a different order.

The corresponding tests in CI are the following:

* ``test_AXI4Stream_OSVVM_VUnit``
* ``test_AXI4Stream_OSVVM_VUnit_WithVCsBefore``
* ``test_AXI4Stream_OSVVM_VUnit_WithVCsAfter``
* ``test_AXI4Stream_OSVVM_VUnit_WithVCsAfterNoSkip``
* ``test_AXI4Stream_OSVVM_VUnit_external_ProFiles``
* ``test_AXI4Stream_OSVVM_VUnit_external_ProFiles_WithVCsBefore``
* ``test_AXI4Stream_OSVVM_VUnit_external_ProFiles_WithVCsAfter``
* ``test_AXI4Stream_OSVVM_VUnit_external_VendorScripts``
* ``test_AXI4Stream_OSVVM_VUnit_external_VendorScripts_WithVCsBefore``
* ``test_AXI4Stream_OSVVM_VUnit_external_VendorScripts_WithVCsAfter``

With pyEDAA.ProjectModel
------------------------

:ref:`edaa:Concept`

*TBC*

.. HINT::
  Probably, use GHDL's :ghrepo:`compile-osvvm.ps1 <ghdl/ghdl/blob/master/scripts/vendors/compile-osvvm.ps1>` as a
  reference or for generating ``*.core`` files automatically.
