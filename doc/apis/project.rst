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

Open Source VHDL Design Explorer (OSVDE)
========================================

OSVDE is GUI for hardware designers to understand and use projects/repositories.
It allows exploring the HDL sources, entities/hierarchies, testbenches, tasks, etc.
It is mostly meant for VHDL designers (but not only) and particularly for users of VHDL >= 2008.

.. IMPORTANT::
  OSVDE is a proof of concept for prototyping the integration of multiple pieces in the OSVB.
  It is not actively developed *per se*, but used as an umbrella for pyVHDLModel, pyGHDL, pyCAPI, etc.

Introduction
------------

`pyVHDLModel <https://github.com/vhdl/pyVHDLModel>`__ is an abstract language model for VHDL written in Python.
That is, a set of classes that represent the objects found in VHDL sources, and utils for manipulating and interacting
with those classes.
The generation of an specific object tree for an specific VHDL codebase is done by a frontend.
Currently supported frontends are `pyGHDL <https://github.com/ghdl/ghdl/tree/master/pyGHDL>`__ and
`pyVHDLParser <https://github.com/Paebbels/pyVHDLParser/>`__.

As a matter of fact, GHDL is the most complete open source VHDL parser and analyser, and more complete than several
vendor tools.
However, GHDL is written in Ada, and it was not initially designed for the analysis features to be used standalone.
Therefore, most developers of tooling around the VHDL language do typically not use GHDL but try reimplementing the
parsing themselves.
That is the case of VUnit, TerosHDL, Symbolator, vhdl-style-guide, VHDLTool, etc.
All of those projects need some understanding of the models they are dealing with, and they use regular expressions,
`tree-sitter <https://github.com/tree-sitter/tree-sitter>`__, `ANTLR <https://www.antlr.org/>`__ or similar general
purpose parser engines.
That is unfortunate because many of them do use Python, so the effort duplication in the community might be
significantly reduced if they could interact with GHDL's parser/analysis through Python.

Since July 2021, pyVHDLModel and pyGHDL provide a ready-to-use solution.
By using those, developers can get a *pythonic* representation of VHDL sources, using less than 10 lines of Python code
which depend on GHDL and Python only.
We believe that projects such as the ones mentioned above could greatly benefit from using pyVHDLModel, as long as they
are good with depending on GHDL.
However, we are aware that reworking an stable codebase is not the most appealing task, so developers will not be
willing to use pyVHDLModel straightaway.
In this context, the main purpose of OSVDE is to showcase pyVHDLModel and to build a critical mass for creating higher
abstraction features on top.
Potential consumers of pyVHDLModel are all the tools which benefit from programmatically using knowledge about a VHDL
codebase.

.. NOTE::
  Projects which don't want to depend on a binary/compiled tool (GHDL), can use a Python only frontend for pyVHDLModel.
  That is precisely the purpose of `pyVHDLParser <https://github.com/Paebbels/pyVHDLParser/>`__ (actually where
  `pyVHDLModel <https://github.com/vhdl/pyVHDLModel>`__ was conceived).
  However, pyVHDLParser is not as mature as (py)GHDL yet.

OSVDE is a GUI tool written in Python only, using `tkinter <https://docs.python.org/3/library/tkinter.html>`__,
*the standard Python interface to the Tk GUI toolkit* (see :py:doc:`faq/gui`).
The motivation for using both Python and tkinter is reducing the dependencies to the bare minimum available on several
plataforms.
As said, the purpose of OSVDE is not to provide the best performance for (very) large designs, but it's for prototyping
the integration of other pieces such as pyCAPI, pydoit and OSVR.

Installation
------------

Install a recent version of GHDL and a matching pyGHDL.
As explained in :ref:`ghdl:USING:QuickStart:Python`, the following pip command can be used:

.. code-block::

   pip3 install git+https://github.com/ghdl/ghdl.git@$(ghdl version hash)

Alternatively, get a tarball/zipfile of the GHDL repository, extract it, and set ``PYTHONPATH`` accordingly.

Then, retrieve this repository (OSVB) and install the dependencies of pyOSVDE:

.. code-block::

   pip3 install mods/pyOSVDE/requirements.txt

Usage
-----

Start OSVDE by executing ``./mods/pyOSVDE/main.py``.
By default, the '*Open Directory...*' is triggered, asking the user to select a directory containing VHDL sources.
Upon selection, the whole directory is scanned recursively, searching for either ``*.vhd`` or ``.osvdeignore`` files,
and all the VHDL sources are added to pyVHDLModel :ref:`vhdlmodel:vhdlmodel-design` as :ref:`vhdlmodel:vhdlmodel-document`
of a :ref:`vhdlmodel:vhdlmodel-library`.
Then, the Design model is used for generating the content of the GUI.

.. HINT::
  Ignore files use the same syntax as regular ``.gitignore`` files, and prevent OSVDE from processing some content.
  In fact, `gitignore-parser <https://pypi.org/project/gitignore-parser/>`__ is used for parsing ``.osvdeignore`` files.

.. ATTENTION::
  Currently, pyGHDL crashes (produces a segmentation fault) if "too many" files are analysed at the same time.
  That is actually a bug, because GHDL itself can handle the same sources for simulation and/or synthesis.
  While the bug is being fixed, it is recommended to use ``.osvdeignore`` files for testing OSVDE with a limited number
  of sources.

.. _fig:osvde:
.. figure:: ../_static/osvde.png
  :alt: Repository NEORV32 opened in OSVDE
  :width: 100%
  :align: center

  Repository `stnolting/neorv32 <https://github.com/stnolting/neorv32>`__ opened in OSVDE.

As shown in :numref:`fig:osvde`, at the top part of OSVDE the hierarchy of the source files is shown.
For each VHDL source, a column shows the units (entities and/or architectures) defined in it.
As a complement, at the bottom part the logical hierarchy of the units is shown, grouped by library.
For each entity, the ports are shown, including the *mode*, the *name* and the *type*.

.. IMPORTANT::
  For now, ``*.vhd`` files are scanned only, and all of them are analysed into library ``lib``.
  That is because the definition of the Filesets and the Project is out of the scope of OSVDE.
  As discussed above, pyCAPI and the project API are to be reused in OSVDE for that purpose.

Future work
-----------

Some enhancements and features we would like to integrate into OSVDE are the following:

* Dependency tree and logic hierarchy elaboration though GHDL.

* Task running/triggering:

  * Discovery of VUnit run scripts (see
    `VSCode TerosHDL <https://marketplace.visualstudio.com/items?itemName=teros-technology.teroshdl>`__,
    `VSCode VUnit Test Explorer <https://marketplace.visualstudio.com/items?itemName=hbohlin.vunit-test-explorer>`__,
    `Sigasi Studio XPRT <https://www.sigasi.com/products/>`__).
  * Discovery of pydoit task definition files (see :ref:`OSVB:API:Tool`).

    * Allow running tasks and showing the results in a window.

  * '*Edit source in editor*' or '*Open project in editor*', where IDE is VSCode, (neo)vim, emacs, notepad++...

* Documentation generation:

  * Entity symbol (see `Symbolator <https://kevinpt.github.io/symbolator/>`__, `xhdl <https://hackfin.gitlab.io/xhdl/>`__).
  * Single page HTML/reStructuredText/markdown body (see `TerosHDL CLI examples <https://github.com/TerosTechnology/teroshdl-documenter-demo>`__).
  * `Sphinx <https://www.sphinx-doc.org>`__ project/domain with cross-references (placeholder: `VHDL/sphinx-vhdl <https://github.com/VHDL/sphinx-vhdl>`__).
  * `Graphviz <https://graphviz.org/>`__/`netlistsvg <https://github.com/nturley/netlistsvg>`__ diagram.

    * For Sphinx (see `sphinxcontrib-hdl-diagrams <https://github.com/SymbiFlow/sphinxcontrib-hdl-diagrams>`__).
    * For asciidoctor (see `Asciidoctor Diagram <https://asciidoctor.org/docs/asciidoctor-diagram/>`__).

* Pretty printing, formatting...

  * Fixed style (see GHDL's :ref:`--pp-html <ghdl:REF:Command>` and `ghdl-dom <https://github.com/ghdl/ghdl/blob/master/pyGHDL/cli/dom.py>`__).
  * Customisable style (see
    `vhdl-style-guide <https://github.com/jeremiah-c-leary/vhdl-style-guide>`__,
    `VHDLTool <https://github.com/VHDLTool>`__).

* pyVHDLModel/pyGHDL enhancements:

  * Preserve comments.
  * Preserve identifier casing.

OSVDE reference
---------------

.. autoclass:: pyOSVDE.main.OSVDE()
  :private-members: False

References
==========

* `EDA integration: managing projects for simulation and implementation <https://docs.google.com/document/d/1qThGGqSVQabts-4imn5zY5BMptp1-Q2rGiNKHDH1Pbk/>`__
* Registers:

  * `tsfpga: Register code generation <https://tsfpga.com/registers.html>`__

  * `cheby <https://gitlab.cern.ch/cohtdrivers/cheby>`__

  * `SystemRDL register description language <https://github.com/SystemRDL>`__
* `dbhi/vsc-hdl <https://github.com/dbhi/vsc-hdl>`__
