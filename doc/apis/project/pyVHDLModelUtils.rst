.. _OSVB:API:Project:pyVHDLModelUtils:

pyVHDLModelUtils
################

pyVHDLModel
===========

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
In this context, the main purpose of :ref:`OSVB:API:Project:OSVDE` is to showcase pyVHDLModel and to build a critical
mass for creating higher abstraction features on top.
Potential consumers of pyVHDLModel are all the tools which benefit from programmatically using knowledge about a VHDL
codebase.

.. NOTE::
  Projects which don't want to depend on a binary/compiled tool (GHDL), can use a Python only frontend for pyVHDLModel.
  That is precisely the purpose of `pyVHDLParser <https://github.com/Paebbels/pyVHDLParser/>`__ (actually where
  `pyVHDLModel <https://github.com/vhdl/pyVHDLModel>`__ was conceived).
  However, pyVHDLParser is not as mature as (py)GHDL yet.

Utils
=====

*TBW*

pyVHDLModelUtils reference
==========================

resolve
-------

.. automodule:: pyVHDLModelUtils.resolve

fmt
---

.. automodule:: pyVHDLModelUtils.fmt

sphinx
------

.. automodule:: pyVHDLModelUtils.sphinx
