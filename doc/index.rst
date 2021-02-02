.. _OSVB:

.. |shieldcocotb| image:: https://img.shields.io/badge/cocotb-77a037.svg?longCache=true&style=flat-square&logo=github
.. _shieldcocotb: https://hdl.github.io/awesome/items/cocotb/

.. |shieldOSVVM| image:: https://img.shields.io/badge/OSVVM-f9ca47.svg?longCache=true&style=flat-square&logo=github&logoColor=000
.. _shieldOSVVM: https://hdl.github.io/awesome/items/osvvm/

.. |shieldSVUnit| image:: https://img.shields.io/badge/SVUnit-488d26.svg?longCache=true&style=flat-square&logo=github
.. _shieldSVUnit: https://hdl.github.io/awesome/items/svunit/

.. |shieldUVVM| image:: https://img.shields.io/badge/UVVM-fe9932.svg?longCache=true&style=flat-square&logo=github
.. _shieldUVVM: https://hdl.github.io/awesome/items/uvvm/

.. |shieldVUnit| image:: https://img.shields.io/badge/VUnit-0c479d.svg?longCache=true&style=flat-square&logo=github
.. _shieldVUnit: https://hdl.github.io/awesome/items/vunit/

.. |shieldGHDL| image:: https://img.shields.io/badge/GHDL-222222.svg?longCache=true&style=flat-square&logo=github
.. _shieldGHDL: https://hdl.github.io/awesome/items/ghdl/

.. |shieldIVerilog| image:: https://img.shields.io/badge/Icarus%20Verilog-f33b48.svg?longCache=true&style=flat-square&logo=github
.. _shieldIVerilog: https://hdl.github.io/awesome/items/iverilog/

.. |shieldVerilator| image:: https://img.shields.io/badge/Verilator-128fd2.svg?longCache=true&style=flat-square&logo=github
.. _shieldVerilator: https://hdl.github.io/awesome/items/verilator/

.. only:: html

    .. centered:: |shieldcocotb|_ |shieldOSVVM|_ |shieldSVUnit|_ |shieldUVVM|_ |shieldVUnit|_ · |shieldGHDL|_ |shieldIVerilog|_ |shieldVerilator|_

    ----

Open Source Verification Bundle
###############################

Welcome to the Documentation of the Open Source Verification Bundle (OSVB)!

OSVB gathers the `most popular <https://larsasplund.github.io/github-facts/>`__ open source verification :ref:`OSVB:Projects`
for VHDL and System Verilog:
`cocotb <https://hdl.github.io/awesome/items/cocotb/>`__,
`OSVVM <https://hdl.github.io/awesome/items/osvvm/>`__,
`SVUnit <https://hdl.github.io/awesome/items/svunit/>`__,
`UVVM <https://hdl.github.io/awesome/items/uvvm/>`__,
`VUnit <https://hdl.github.io/awesome/items/vunit/>`__.
Each of them was created and is maintained by different groups of people, in different contexts and with different backgrounds.
All evolved into standalonish solutions involving build and test execution helpers, along with verification components for
standard interfaces. However, each project prioritised certain features, while others didn't receive so much care. The purpose
of this bundle is twofold:

* Allow users of any of the frameworks/methodologies to share some plumbing with others, so that communities can share
  testbenches written in any framework without having to learn a new workflow from scratch.
* Reduce the maintenance burden of the projects by focusing on the features which are unique to a particular
  framework/methodology, instead of reinventing the wheel.

All the frameworks support multiple vendor tools as well as open source simulators. However, due to licensing restrictions,
it is not possible to test non FLOSS simulators on public Continuous Integration (CI) services. Therefore, the examples
in this bundle are tested on CI with open source simulators/compilers only (see :ref:`OSVB:Simulators`).

.. IMPORTANT:: This project is a proof of concept for gathering several integration efforts involving the target projects by
  pairs. For instance, VUnit and cocotb, or VUnit and OSVVM. Not all the features described in this home page are implemented
  yet. See the available examples for an specific reference about what is ready to be used.

.. toctree::
  :caption: Introduction
  :hidden:

  intro/index
  intro/frameworks
  intro/sim
  intro/cosim

.. toctree::
  :caption: API
  :hidden:

  apis/core
  apis/project
  apis/tool
  apis/runner
  apis/logging

.. toctree::
  :caption: Examples
  :hidden:

  egs/sff
  egs/axi4stream
