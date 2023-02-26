.. _API:Project:pyVHDLModelUtils:

pyVHDLModelUtils
################

pyVHDLModel
===========

:gh:`vhdl/pyVHDLModel` is an abstract language model for VHDL written in Python.
That is, a set of classes that represent the items found in VHDL sources, and utils for manipulating and interacting
with those classes.
The generation of an specific object tree for an specific VHDL codebase is done by a frontend.
Currently supported frontends are :gh:`pyGHDL <ghdl/ghdl/tree/master/pyGHDL>` and :gh:`Paebbels/pyVHDLParser`.

GHDL is the most complete open source VHDL parser and analyser, and more complete than several vendor tools.
However, GHDL is written in Ada, and it was not initially designed for the analysis features to be used standalone.
Therefore, most developers of tooling around the VHDL language do typically not use GHDL but try reimplementing the
parsing themselves.
That is the case of
:web:`VUnit <vunit.github.io>`,
:web:`TerosHDL <terostech.com>`,
:web:`Symbolator <kevinpt.github.io/symbolator>`,
:web:`vhdl-style-guide <vhdl-style-guide.readthedocs.io/>`,
:gh:`VHDLTool`,
:gh:`Nic30/hdlConvertor`,
etc.
All of those projects need some understanding of the models they are dealing with, and they use regular expressions,
:gh:`tree-sitter/tree-sitter`, :web:`ANTLR <www.antlr.org/>` or similar general purpose parser engines.
That is unfortunate because many of them do use Python, so the effort duplication in the community might be
significantly reduced if they could interact with GHDL's parser/analysis through Python.

Since 2021, pyVHDLModel and pyGHDL provide a ready-to-use solution.
By using those, developers can get a *pythonic* representation of VHDL sources, using less than 10 lines of Python code
which depend on GHDL and Python only.
We believe that projects such as the ones mentioned above could greatly benefit from using pyVHDLModel, as long as they
are good with depending on GHDL.

.. NOTE::
  Projects which don't want to depend on a binary/compiled tool (GHDL), can use a Python only frontend for pyVHDLModel.
  That is precisely the purpose of :gh:`pyVHDLParser <Paebbels/pyVHDLParser>` (actually where
  :gh:`pyVHDLModel <vhdl/pyVHDLModel>` was conceived).
  However, pyVHDLParser is not as mature as (py)GHDL yet.

Utils
=====

pyVHDLModel and pyGHDL are still being shaped and enhanced in order to provide higher abstraction features on top of parsing.
Moreover, there are some helper functions written on top of pyVHDLModel, which don't fit in the same repository but can
be reused by multiple projects.
:ghsrc:`pyVHDLModelUtils <mods/pyVHDLModelUtils>` collects some of those helpers, until we decide a better location for them.

.. NOTE::
  We are aware that reworking an stable codebase is not the most appealing task, so developers of existing tools might
  not be willing to use pyVHDLModel straightaway.
  In this context, the main purpose of pyVHDLModelUtils, :ref:`API:Project:OSVDE` and :ref:`API:Project:DocGen`
  is to showcase pyVHDLModel and to build a critical mass for creating higher abstraction features on top.
  Potential users of pyVHDLModel are all the developers of tools which benefit from programmatically using knowledge
  about a VHDL codebase.

pyVHDLModelUtils reference
==========================

resolve
-------

Currently, pyVHDLModel and pyGHDL.dom provide a SyntaxModel only.
That is, the model is built from parsing the sources, without further analysis or elaboration.
As a result, symbols and cross-references between units are not resolved.
This package provides some *naive* Symbol resolution features.
In the future, we expect to use pyGHDL.libghdl for elaboration.

.. automodule:: pyVHDLModelUtils.resolve

fmt
---

Getting an string representation of some elements such as (sub)types might be cumbersome.
This package handles formatting those.

.. automodule:: pyVHDLModelUtils.fmt

sphinx
------

Since Sphinx is written in Python, packages can be imported and used for generating content.
This package provides functions for including the documentation of hardware designs in Sphinx projects.

.. automodule:: pyVHDLModelUtils.sphinx
