.. _API:Project:DocGen:

Documentation generation
########################

Automatic documentation generation of hardware designs is one of the main purposes of having a machine-readable project
description format along with a library providing a Document Object Model (DOM).
Some of the features to be implemented on top of :ref:`API:Project:pyVHDLModelUtils` are the following:

* Entity symbol:

  * :web:`Symbolator <kevinpt.github.io/symbolator/>`

    * :gh:`hdl/symbolator`
    * :gh:`hdl/pyHDLParser`

  * :web:`schemdraw.rtfd.io: Circuit Elements » Integrated Circuits <schemdraw.readthedocs.io/en/stable/elements/intcircuits.html>`

  * :web:`xhdl <hackfin.gitlab.io/xhdl/>`
  * :gh:`LaurentCabaret/pyVhdl2Sch`

* Single page HTML/reStructuredText/markdown body (see :gh:`TerosHDL CLI examples <TerosTechnology/teroshdl-documenter-demo>`).
* :web:`Sphinx <www.sphinx-doc.org>` project/domain with cross-references (placeholder: :gh:`Paebbels/sphinxcontrib-vhdldomain`).
* Diagrams:

  * For Sphinx (see :ref:`Integration with Sphinx » Diagrams <API:Project:DocGen:Sphinx:Diagrams>`).
  * For asciidoctor (see :web:`Asciidoctor Diagram <asciidoctor.org/docs/asciidoctor-diagram/>`).

.. _API:Project:DocGen:Sphinx:

Integration with Sphinx
=======================

:web:`Sphinx <www.sphinx-doc.org>` is the *de facto* static site generator (SSG) used for building documentation of
Python projects.
It was originally created for :doc:`Python <py:contents>`, and it has support for documenting software projects in several
languages. Since many open source EDA projects and CLIs are written in Python, Sphinx is probably the most used SSG.
It's used by SymbiFlow, GHDL, VUnit, pyVHDLModel/pyVHDLParser, cocotb, TerosHDL, Boolector, edalize/fusesoc,
Wishbone (FOSSi), SpinalHDL, tsfpga...

Additional features can be added to Sphinx through :web:`extensions <www.sphinx-doc.org/en/master/usage/extensions/index.html>`.
For instance, :web:`intersphinx <www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>` allows
cross-referencing content across sites, as if they were local references.
That is really handy for building knowledge as a community.

The default plaintext markup language used by Sphinx is :web:`reStructuredText <docutils.sourceforge.io/rst.html>`.
Other markup languages, such as Markdown, can be imported through extensions, however, not all cross-reference features
are available when using those.

Overall, there are four approaches for adding content with custom processing to a site built with Sphinx:

* Execute before Sphinx:

  * `html_static_path`: content in the *static* paths is copied to the output's `_static` directory, overriding existing
    sources with the same name.
    This is typically used for adding images and/or customising the CSS.
  * `html_extra_path`: content in *extra* paths is copied as-is to the output directory, overriding existing sources
    with the same name.
    This can be used for adding static content generated with a different generator.

* Built into Sphinx:

  * `exec`: a generic directive (such as the ones proposed in :web:`stackoverflow.com/a/18143318`)
    allows executing arbitrary Python code which generates reStructuredText output through `print` statements.
  * Ad-hoc directive: as explained in :web:`Developing extensions for Sphinx <www.sphinx-doc.org/en/master/extdev/index.html#dev-extensions>`,
    there are several objects whose API can be used when writing extensions: Application, Environment, Builder and Config.
    Those allow fine-grained integration into Sphinx's internals, potentially bypassing the reStructuredText parsing
    layer.
    This is the end-goal for tightly integrated and customised functionality.

.. _API:Project:DocGen:Sphinx:exec:

*exec* directive
----------------

The generic `exec` extension (see :ghsrc:`doc/exec.py <doc/exec.py>`) is based on :web:`stackoverflow.com/a/18143318`.
It allows executing arbitrary Python code which prints reStructuredText output.

Setup is done by adding `exec` to the `extensions` variable of the ``conf.py``.
Depending on the location of `exec.py`, it might be necessary to add ``sys.path.insert(0, abspath("."))``.
Other than that, users (developers of the arbitrary Python code) don't need to know internals of Sphinx, but just print
regular reStructuredText statements.

However, a main caveat of the current implementation is that Sphinx will never fail.
That is, even if the arbitrary code fails, the Sphinx build is reported as successful.
That's because errors are shown as an admonition instead of making the build fail.
As a result, manual inspection of the output is required (desirable).

Moreover, currently no context is passed to the Python code.
Therefore, it is not possible to know where it belongs in the hierarchy of the document.
This is a limitation for generating headers and other context dependent statements.

.. NOTE::
  Should you want to help improve the implementation of this directive, :gh:`let us know <umarcor/osvb/issues/new>`!

Lists and tables
----------------

This section showcases a naive approach for documenting VHDL design units using pyGHDL.dom.
It is based on :ref:`API:Project:DocGen:Sphinx:exec` and the ``sphinx`` module of :ref:`API:Project:pyVHDLModelUtils`.

First, `initDesign` needs to be executed, in order to provide the lists of sources and VHDL library names.

.. NOTE::
  Currently, there is no specific JSON/YAML format supported for this task.
  Find work in progress in section :ref:`API:Core`.

.. code-block:: python
  :caption: Loading design sources.

  .. exec::
     from pyVHDLModelUtils.sphinx import initDesign
     initDesign(
       '..',
       AXI4 = ["AXI4Stream/src/*.vhd"],
       fpconv = ["fpconv/*.vhd"]
     )

The output of *initDesign* is a NOTE containing the result of parsing the sources with pyGHDL.dom.
If a failure was produced, an admonition of type ERROR is shown instead.

.. exec::
   from pyVHDLModelUtils.sphinx import initDesign
   initDesign(
     '..',
     AXI4 = ["AXI4Stream/src/*.vhd"],
     fpconv = ["fpconv/*.vhd"]
   )

Then, `printDocumentationOf` allows generating the documentation of libraries and/or design units.
By default, the content is shown where the directive was called.
In case of failure, an admonition of type ERROR is shown.

.. code-block:: python
  :caption: Printing a summary of the content.

  .. exec::
     from pyVHDLModelUtils.sphinx import printDocumentationOf
     printDocumentationOf()

.. exec::
   from pyVHDLModelUtils.sphinx import printDocumentationOf
   printDocumentationOf()

At the moment, two different styles are supported for printing the documentation of entities.

List style:

.. code-block:: python
  :caption: Printing the documentation of a unit (style 'rst:list').

  .. exec::
     from pyVHDLModelUtils.sphinx import printDocumentationOf
     printDocumentationOf(["AXI4.axis_buffer"])

.. exec::
   from pyVHDLModelUtils.sphinx import printDocumentationOf
   printDocumentationOf(["AXI4.axis_buffer"])

Table style:

.. code-block:: python
  :caption: Printing the documentation of a unit (style 'rst:table').

  .. exec::
     from pyVHDLModelUtils.sphinx import printDocumentationOf
     printDocumentationOf(
       ["AXI4.axis_buffer"],
       'rst:table'
     )

.. exec::
   from pyVHDLModelUtils.sphinx import printDocumentationOf
   printDocumentationOf(
     ["AXI4.axis_buffer"],
     'rst:table'
   )

.. NOTE::
  This is a demo for showcasing the capabilities of pyGHDL.dom and pyVHDLModel.
  Should you want to help improve the implementation for it to be more usable in practice, :gh:`let us know <umarcor/osvb/issues/new>`!

VHDL Domain
-----------

:gh:`Paebbels/sphinxcontrib-vhdldomain` is work in progress for adding a VHDL language domain to Sphinx.
That is, a set of nestable directives resembling the architecture of pyVHDLModel.
The purpose is twofold:

* Allow a better integration of the content into Sphinx, rather than generating reStructuredText output from arbitrary
  Python functions.
* Allow users to specify a pyVHDLModel project by handwriting directives in reStructuredText sources, by either pointing
  to individual files or explicitly describing all the items.

See :gh:`Paebbels/sphinxcontrib-vhdldomain#4 <Paebbels/sphinxcontrib-vhdldomain/issues/4>`.

There is also :gh:`CESNET/sphinx-vhdl`, which uses a custom basic parser (:gh:`CESNET/sphinx-vhdl: src/sphinxvhdl/autodoc.py <CESNET/sphinx-vhdl/blob/main/src/sphinxvhdl/autodoc.py>`)
and multiple custom Sphinx directives (:gh:`CESNET/sphinx-vhdl: src/sphinxvhdl/vhdl.py <CESNET/sphinx-vhdl/blob/main/src/sphinxvhdl/vhdl.py>`).

.. _API:Project:DocGen:Sphinx:Diagrams:

Diagrams
--------

Both GHDL and Yosys allow generating diagrams of synthesised designs.

* ``ghdl synth --out=dot`` generates a :web:`Graphviz <graphviz.org/>` DOT diagram of the netlist AST.

* :gh:`ghdl/ghdl-yosys-plugin` allows using GHDL as a frontend for Yosys.

  * As explained in :ref:`ghdl.github.io/ghdl/synthesis » Yosys plugin <ghdl:Synth:plugin>`, ghdl-yosys-plugin and Yosys
    allow converting VHDL to EDIT, SMT, BTOR2, FIRRTL, etc.

* Yosys's :web:`show <yosyshq.net/yosys/cmd_show.html>` command allows generating a Graphviz DOT diagram and compiling
  it to a graphics file (say SVG).

  * Optionally, command :web:`aigmap <yosyshq.net/yosys/cmd_aigmap.html>` can map the logic to and/nand gates only,
    before generating the diagram.

  * Alternatively, :gh:`nturley/netlistsvg` allows generating SVG schematics from Yosys' JSON netlist output.

By combining those tools, diagrams of a given VHDL design can be generated as follows:

.. code-block:: shell

  ~# yosys -p 'ghdl --std=08 design.vhd -e primary_unit secondary_unit; prep; write_json netlist.json'
  ~# netlistsvg netlist.json -o netlist.svg
  ~# convert netlist.svg netlist.png

.. IMPORTANT::
  There is an Sphinx extension named :gh:`sphinxcontrib-hdl-diagrams <SymbiFlow/sphinxcontrib-hdl-diagrams>`,
  which wraps Yosys and (optionally) netlistsvg in a directive.
  That allows including diagrams in the docs without manually calling yosys and netlistsvg.
  For instance:

  .. code-block:: restructuredtext

     .. hdl-diagram:: file.v
        :type: netlistsvg
        :module: name
        :flatten:

  However, since sphinxcontrib-hdl-diagrams depends on combining the WASM version of Yosys and netlistsvg (which is
  JavaScript), it does not support VHDL yet.
  There is work in progress for using the extension with "natively" installed tools, as well as supporting VHDL and
  mixed-language designs.
  See
  :gh:`SymbiFlow/sphinxcontrib-hdl-diagrams#65 <SymbiFlow/sphinxcontrib-hdl-diagrams/issues/65>`,
  :gh:`SymbiFlow/sphinxcontrib-hdl-diagrams#72 <SymbiFlow/sphinxcontrib-hdl-diagrams/pull/72>`
  and :gh:`SymbiFlow/sphinxcontrib-hdl-diagrams#73 <SymbiFlow/sphinxcontrib-hdl-diagrams/pull/73>`.

References
==========

* :bb:`cdelker/schemdraw` (:web:`schemdraw.rtfd.io`).
