.. _OSVB:API:Project:OSVDE:

Open Source VHDL Design Explorer (OSVDE)
########################################

OSVDE is GUI for hardware designers to understand and use projects/repositories.
It allows exploring the HDL sources, entities/hierarchies, testbenches, tasks, etc.
It is mostly meant for VHDL designers (but not only) and particularly for users of VHDL >= 2008.

.. IMPORTANT::
  OSVDE is a proof of concept for prototyping the integration of multiple pieces in the OSVB.
  It is not actively developed *per se*, but used as an umbrella for pyVHDLModel, pyGHDL, pyCAPI, etc.
  A practical usage of the features prototyped in OSVDE is found in `Hardware Studio <https://github.com/umarcor/hwstudio>`__
  (see `umarcor.github.io/hwstudio/doc: Structure <https://umarcor.github.io/hwstudio/doc/#_structure>`__).

OSVDE is a GUI tool written in Python only, using `tkinter <https://docs.python.org/3/library/tkinter.html>`__,
*the standard Python interface to the Tk GUI toolkit* (see :py:doc:`faq/gui`).
The motivation for using both Python and tkinter is reducing the dependencies to the bare minimum available on several
plataforms.
As said, the purpose of OSVDE is not to provide the best performance for (very) large designs, but it's for prototyping
the integration of other pieces such as pyCAPI, pydoit and OSVR.

Installation
============

Install a recent version of GHDL and a matching pyGHDL.
As explained in :ref:`ghdl:USING:QuickStart:Python`, the following pip command can be used:

.. code-block::

   pip3 install git+https://github.com/ghdl/ghdl.git@$(ghdl version hash)

Alternatively, get a tarball/zipfile of the GHDL repository, extract it, and set ``PYTHONPATH`` accordingly.

Then, retrieve this repository (OSVB) and install the dependencies of pyOSVDE:

.. code-block::

   pip3 install -r mods/pyOSVDE/requirements.txt

Usage
=====

Start OSVDE by executing ``PYTHONPATH=$(pwd)/mods ./mods/pyOSVDE/main.py``.
By default, the '*Open Directory...*' is triggered, asking the user to select a directory containing VHDL sources.
Upon selection, the whole directory is scanned recursively, searching for either ``*.vhd*`` or ``.osvdeignore`` files,
and all the VHDL sources are added to pyVHDLModel :ref:`vhdlmodel:vhdlmodel-design` as a :ref:`vhdlmodel:vhdlmodel-document`
of a :ref:`vhdlmodel:vhdlmodel-library`.
Then, the Design model is used for generating the content of the GUI.

.. HINT::
  Ignore files use the same syntax as regular ``.gitignore`` files, and prevent OSVDE from processing some content.
  In fact, `gitignore-parser <https://pypi.org/project/gitignore-parser/>`__ is used for parsing ``.osvdeignore`` files.

.. ATTENTION::
  Currently, pyGHDL may crash (produce a segmentation fault) if "too many" files are analysed at the same time.
  That is actually a bug, because GHDL itself can handle the same sources for simulation and/or synthesis.
  While the bug is being fixed, it is recommended to use ``.osvdeignore`` files for testing OSVDE with a limited number
  of sources.

.. _fig:osvde:
.. figure:: ../../_static/osvde.png
  :alt: Repository NEORV32 opened in OSVDE
  :width: 100%
  :align: center

  Repository `stnolting/neorv32 <https://github.com/stnolting/neorv32>`__ opened in OSVDE.

As shown in :numref:`fig:osvde`, at the top part of OSVDE the hierarchy of the source files is shown.
For each VHDL source, a column shows the units (entities and/or architectures) defined in it.
As a complement, at the bottom part the logical hierarchy of the units is shown, grouped by library.
For each entity, the generics and ports are shown, including the *name*, *type* and (for ports only) *mode*.
Architectures are shown too, and within them concurrent statements such as instantiations and generates.

.. IMPORTANT::
  For now, ``*.vhd*`` files are scanned only, and all of them are analysed into library ``lib``.
  That is because the definition of the Filesets and the Project is out of the scope of OSVDE.
  As discussed above, pyCAPI and the project API are to be reused in OSVDE for that purpose.

Future work
===========

Some enhancements and features we would like to integrate into OSVDE are the following:

* Dependency tree and logic hierarchy elaboration through GHDL.

* Task running/triggering:

  * Discovery of VUnit run scripts (see
    `VSCode TerosHDL <https://marketplace.visualstudio.com/items?itemName=teros-technology.teroshdl>`__,
    `VSCode VUnit Test Explorer <https://marketplace.visualstudio.com/items?itemName=hbohlin.vunit-test-explorer>`__,
    `Sigasi Studio XPRT <https://www.sigasi.com/products/>`__).
  * Discovery of pydoit task definition files (see :ref:`OSVB:API:Tool`).

    * Allow running tasks and showing the results in a window.

  * '*Edit source in editor*' or '*Open project in editor*', where IDE is VSCode, (neo)vim, emacs, notepad++...

* :ref:`OSVB:API:Project:DocGen`.

* Pretty printing, formatting...

  * Fixed style (see GHDL's :ref:`--pp-html <ghdl:REF:Command>` and `ghdl-dom <https://github.com/ghdl/ghdl/blob/master/pyGHDL/cli/dom.py>`__).
  * Customisable style (see
    `vhdl-style-guide <https://github.com/jeremiah-c-leary/vhdl-style-guide>`__,
    `VHDLTool <https://github.com/VHDLTool>`__).
  * `AdiuvoEngineering/VHDL_Coding_Rules <https://github.com/AdiuvoEngineering/VHDL_Coding_Rules>`__.

* pyVHDLModel/pyGHDL enhancements:

  * Preserve comments.
  * Preserve identifier casing.

OSVDE reference
===============

.. autoclass:: pyOSVDE.main.OSVDE()
  :private-members: False
