.. _API:Project:

Project
#######

This section covers the definition of an API for binding the sources and options from the :ref:`API:Core` to the
interfaces in :ref:`API:Tool`, :ref:`API:Runner` and :ref:`API:Logging`.
The Project and Design management API handles tools independent information (files/filesets, primary design units,
testbenches, constraints, etc.) and some tool specific parameters.

* Project: a set of sources (HDL, software, data, assets, configuration files, etc.) for handling multiple designs.
* Design: a design unit, the dependencies, the parent units (testbenches and BoardTop) and the parameters for execution.

This is probably the most complex piece, because it is the less constrained.
Interaction with tools and manipulation of file formats are technically limited by the interfaces and capabilities in
those.
Therefore, although there is flexibility in the implementation of :ref:`API:Core`, :ref:`API:Tool`,
:ref:`API:Runner` and :ref:`API:Logging`, all of them need to match some external resource.
Conversely, defining what a project is and how to handle it tends to be specific for each use case (say organisation,
company, open source project...), so there is a vast space of different workflows, all similar but particular enough.
Therefore, the elaboration of the API in this section is delayed until others are defined, since that will allow working
on a finite scope.

Nevertheless, there are some features available already for dealing with "whole repositories" of VHDL sources.
The proofs of concept below showcase pyGHDL.dom, the Python Document Object Model (DOM) interface built on top of GHDL's
parsing capabilities.

.. toctree::
  :caption: Proofs of concept

  project/pyVHDLModelUtils
  project/OSVDE
  project/DocGen

References
==========

* :gdocs:`EDA integration: managing projects for simulation and implementation <1qThGGqSVQabts-4imn5zY5BMptp1-Q2rGiNKHDH1Pbk>`

* Registers:

  * :web:`tsfpga: Register code generation <tsfpga.com/registers.html>`
  * :web:`cheby <gitlab.cern.ch/cohtdrivers/cheby>`
  * :ghrepo:`SystemRDL register description language <SystemRDL>`
  * :ghrepo:`RgGen <rggen/rggen>`
  * :ghrepo:`wzab/agwb`
  * :web:`airhdl <airhdl.com>`

* :ghrepo:`dbhi/vsc-hdl`

* :ghrepo:`orestesmas/pycirkuit`

* :ghrepo:`pieter3d/simview`
