.. _OSVB:API:Project:

Project
#######

This section covers the definition of an API for binding the sources and options from the :ref:`OSVB:API:Core` to the
interfaces in :ref:`OSVB:API:Tool`, :ref:`OSVB:API:Runner` and :ref:`OSVB:API:Logging`.
The Project management API is responsible for deciding which tasks to execute, the order, and the file dependencies and
artifacts.

This is probably the most complex piece of all the API sections, because it is the less constrained.
Interaction with tools and manipulation of file formats are technically limited by the interfaces and capabilities in
those.
Therefore, although there is flexibility in the implementation of :ref:`OSVB:API:Core`, :ref:`OSVB:API:Tool`,
:ref:`OSVB:API:Runner` and :ref:`OSVB:API:Logging`, all of them need to match some external resource.
Conversely, defining what a project is and how to handle it needs to be specific for each use case (say organisation,
company, open source project...), so there is a vast space of different workflows, all similar but particular enough.
Therefore, the elaboration of the API in this section is delayed until others are defined, since that will allow working
on a finite scope.

.. toctree::
  :caption: Proofs of concept

  project/pyVHDLModelUtils
  project/OSVDE
  project/DocGen

References
==========

* `EDA integration: managing projects for simulation and implementation <https://docs.google.com/document/d/1qThGGqSVQabts-4imn5zY5BMptp1-Q2rGiNKHDH1Pbk/>`__

* Registers:

  * `tsfpga: Register code generation <https://tsfpga.com/registers.html>`__
  * `cheby <https://gitlab.cern.ch/cohtdrivers/cheby>`__
  * `SystemRDL register description language <https://github.com/SystemRDL>`__
  * `RgGen <https://github.com/rggen/rggen>`__
  * `wzab/agwb <https://github.com/wzab/agwb>`__
  * `airhdl <https://airhdl.com>`__

* `dbhi/vsc-hdl <https://github.com/dbhi/vsc-hdl>`__

* `orestesmas/pycirkuit <https://github.com/orestesmas/pycirkuit>`__
