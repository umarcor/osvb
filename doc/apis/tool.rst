.. _OSVB:API:Tool:

Tool
####

This section covers the interface for interacting with EDA tools. Since each tool has different mechanisms for achieving
the same results, the purpose of this interface is to provide homogeneous wrapper interfaces that the
:ref:`OSVB:API:Project` can use.

*TBC*

.. NOTE:: As shown in the diagram of section :ref:`OSVB:API:Core`, developers of Edalize and PyFPGA have been lately
  working towards making integration easier. On the one hand, experimental support for *launchers* was added to Edalize
  (`olofk/edalize@f8b3f66 <https://github.com/olofk/edalize/commit/f8b3f666a282e09b8ce06388101d179f8c70e8d4>`__). That
  allows wrapping the lower level commands. On the other hand, `OpenFlow <https://github.com/PyFPGA/openflow>`__ was
  split from PyFPGA. OpenFlow wraps (Docker/Podman) containers, allowing usage of EDA tools without installing them
  natively. By default, containers from `hdl/containers <https://github.com/hdl/containers>`__ are used. By combining
  both solutions, users can use Edalize with containers.

References
==========

* `Open Source EDA: building, packaging, installing <https://docs.google.com/document/d/10_MqFjTIYVVuOJlusJydsp4KOcmrrHk03__7ME5thOI>`__
* `Invoke <http://www.pyinvoke.org/>`__
* `dbhi/run <https://github.com/dbhi/run>`__
* SymbiFlow

  * `SymbiFlow Publically Accessible Docs <https://drive.google.com/drive/folders/1euSrrszzt3Bfz792S6Ud8Ox2w7TYUZNa>`__
  * `bit.ly/edda-conda-eda-spec: Conda based system for FPGA and ASIC Dev <https://docs.google.com/document/d/1BZcSzU-ur0J02uO5FSGHdJHYGnRfr4n4Cb7PMubXOD4>`__
  * `Next Conda Work <https://docs.google.com/document/d/11XFnJ0ExBgE1pMQksw0rQerAZo3F83AVIu2YK1pbg1k>`__
  * `SymbiFlow/make-env <https://github.com/SymbiFlow/make-env>`__
  * `edalize.autosetup <https://docs.google.com/document/d/1IMVrSmMO5wqTV3W22Bv2PeKtMHO3WSyCwHm3N-Wkwbk>`__
