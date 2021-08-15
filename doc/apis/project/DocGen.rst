.. _OSVB:API:Project:DocGen:

Documentation generation
########################

Automatic documentation generation of hardware designs is one of the main purposes of having a machine-readable project
description format along with a library providing a DOM.
Some of the features to be implemented on top of :ref:`OSVB:API:Project:pyVHDLModelUtils` are the following:

* Entity symbol (see `Symbolator <https://kevinpt.github.io/symbolator/>`__, `xhdl <https://hackfin.gitlab.io/xhdl/>`__).
* Single page HTML/reStructuredText/markdown body (see `TerosHDL CLI examples <https://github.com/TerosTechnology/teroshdl-documenter-demo>`__).
* `Sphinx <https://www.sphinx-doc.org>`__ project/domain with cross-references (placeholder: `Paebbels/sphinxcontrib-vhdldomain <https://github.com/Paebbels/sphinxcontrib-vhdldomain/>`__).
* `Graphviz <https://graphviz.org/>`__/`netlistsvg <https://github.com/nturley/netlistsvg>`__ diagram.

  * For Sphinx (see `sphinxcontrib-hdl-diagrams <https://github.com/SymbiFlow/sphinxcontrib-hdl-diagrams>`__).
  * For asciidoctor (see `Asciidoctor Diagram <https://asciidoctor.org/docs/asciidoctor-diagram/>`__).

Integration with Sphinx
=======================

.. code-block:: python
  :caption: Loading design sources.

  .. exec::
     from pyVHDLModelUtils.sphinx import initDesign
     initDesign(
       '..',
       AXI4 = ["AXI4Stream/src/*.vhd"],
       fpconv = ["fpconv/*.vhd"]
     )

.. exec::
   from pyVHDLModelUtils.sphinx import initDesign
   initDesign(
     '..',
     AXI4 = ["AXI4Stream/src/*.vhd"],
     fpconv = ["fpconv/*.vhd"]
   )


.. code-block:: python
  :caption: Printing a summary of the content.

  .. exec::
     from pyVHDLModelUtils.sphinx import printDocumentationOf
     printDocumentationOf()

.. exec::
   from pyVHDLModelUtils.sphinx import printDocumentationOf
   printDocumentationOf()

.. code-block:: python
  :caption: Printing the documentation of a unit (style 'rst:list').

  .. exec::
     from pyVHDLModelUtils.sphinx import printDocumentationOf
     printDocumentationOf(["AXI4.axis_buffer"])

.. exec::
   from pyVHDLModelUtils.sphinx import printDocumentationOf
   printDocumentationOf(["AXI4.axis_buffer"])


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
