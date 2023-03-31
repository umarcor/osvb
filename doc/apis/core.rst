.. _API:Core:

Core
####

This section covers the definition of configuration/declaration files for users to describe the sources and parameters
that compose an HDL project.
Several JSON/YAML/INI formats are supported by different tools in the ecosystem.
Here, we don't want to focus as much on the specific file format as we do want to understand the structure of the data.
A Python module is proposed for interacting with those file formats.

Introduction
------------

:awesome:`FuseSoC <fusesoc>` is a package manager and build abstraction tool for FPGA/ASIC development, written in
Python. It is based on a declarative data sctructure, defined as a YAML configuration file format named Core API (CAPI).
The current version 2 of the format is named ``CAPI2`` (see :web:`fusesoc.rtfd.io: ref/capi2 <fusesoc.rtfd.io/en/latest/ref/capi2.html>`).
A single YAML file can be used for defining all the sources and parameters related to multiple tools for simulation,
verification, synthesis, etc.

Initially, FuseSoC was a monolith that allowed interacting with FPGA/ASIC tools directly.
Later, :awesome:`Edalize <edalize>` was split, and an API named EDA Metadata (EDAM) was proposed for the interaction
from FuseSoC or other frontends.
:awesome:`Hdlmake <hdlmake>` is one of the projects that can use Edalize through EDAM.

Nevertheless, the proposal for funneling all open source project management tools through Edalize didn't engage the
broad open source hardware tooling community. Multiple projects (such as
:awesome:`VUnit <vunit>`,
:awesome:`pyIPCMI <pyipcmi>`,
:awesome:`PyFPGA <pyfpga>`,
:awesome:`tsfpga <tsfpga>`
or
:awesome:`Xeda <xeda>`
) provide independent APIs and CLIs for interacting with FPGA/ASIC tools.
Most of them are also standalone monoliths with custom configuration file formats.
Therefore, workflows are not compatible, and users need duplicated configurations for addressing the requirements of
each tool.

There have been some integration efforts; for instance, supporting VUnit scripts as FuseSoC/Edalize targets.
However, there is a paradigm conflict, since FuseSoC expects to be the entrypoint and Edalize is to be the backend.
Therefore, integration of other tools is only conceived as plugins in the already constrained framework.
Doing so breaks the workflows that the user bases of other projects do rely on.

The proposal in this bundle is to provide a reusable Python module named pyCAPI, for reading CAPI files and manipulating
the data through a pythonic API.
pyCAPI allows FPGA/ASIC tool management projects to consume ``*.core`` configuration files non-intrusively, by providing
complementary import APIs.
Thus the CLIs in the existing workflows are preserved, without forcing FuseSoC as a frontend and/or Edalize as a
backend.
Hopefully, pyCAPI reduces the burden for users to try and learn new tools, while developers/maintainers can carefully
analyse possible integration strategies with regard to the other APIs in the architecture.

.. figure:: ../_static/pyCAPI.png
  :alt: pyCAPI usage block diagram
  :align: center

  Usage of pyCAPI as a utility library for multiple EDA management projects.

FuseSoC does contain some Python code for reading and parsing CAPI2 files (see :gh:`olofk/fusesoc: fusesoc/capi2 <olofk/fusesoc/tree/master/fusesoc/capi2>`).
Unfortunately, it is challenging to work with.
On the one hand, it uses :web:`pyyaml <pyyaml.org>` for reading ``*.core`` files as Python dictionaries and lists.
As a result, the procedure for providing Python classes is manual and prone to error.
On the other hand, the format is documented in the sources of the code, but the code itself is undocumented.

Conversely, pyCAPI is a proof of concept based on Python :mod:`python:dataclasses` for direct (un)marshalling of YAML
to/from Python classes.
Hence, the CAPI2 format is not supported as-is yet: some non compliant fields were modified, and the prototype is
limited to reading filesets.
This work-in-progress version of CAPI is marked as ``3``, for avoiding conflicts with existing ``*.core`` files.
Still, pyCAPI does already allow VUnit to read ``*.core`` files for declaring HDL sources and the ``logical_name`` of
the libraries where they need to be compiled.
I.e., it allows providing a working proof of concept, constrainted to the simulation/verification scope of this bundle.

Feedback and contributions for making pyCAPI compatible with and supported by FuseSoC, VUnit, PyFPGA, pyIPCMI, etc. are
very welcome!
:gh:`Open an issue <umarcor/osvb/issues/new/choose>` or :web:`join the chat <gitter.im/hdl/community>`!

CAPI reference
--------------

.. autoclass:: pyCAPI.IpCoreConfig()

.. autoclass:: pyCAPI.FilesetConfig()

.. autoclass:: pyCAPI.Config()

.. autofunction:: pyCAPI.LoadCoreFile

.. autofunction:: pyCAPI.VUnit.AddCoreFilesets

References
----------

* :gh:`yukihiko-shinoda/yaml-dataclass-config`
* :web:`su0.io: Strict YAML deserialization with marshmallow <su0.io/2020/08/05/python-strict-yaml-deserialization.html>`
* :gh:`antonblanchard/microwatt: microwatt.core <antonblanchard/microwatt/blob/master/microwatt.core>`
* :gh:`VLSI-EDA/PoC: .pyIPCMI <VLSI-EDA/PoC/tree/master/.pyIPCMI>`
* :gdocs:`j.mp/openfpga-diagram: Open Source (FOSS) FPGA (EDA) Tooling Interchange Formats + Toolchain parts <1DWZ0G8vehkuZTPs5N3AQqIvZZtLMGzC8i0MWPRP54O4>`
* :gh:`ghdl/ghdl-language-server#12 <ghdl/ghdl-language-server/issues/12>` :gh:`ghdl/ghdl-language-server#80 <ghdl/ghdl-language-server/issues/80>`
* :gh:`cocotb[wiki]: Python Test Runner Proposal | Models <cocotb/cocotb/wiki/Python-Test-Runner-Proposal#models>`.
* :gh:`Core HAMMER settings <ucb-bar/hammer/blob/master/src/hammer-vlsi/defaults.yml>`
* :gh:`kactus2/kactus2dev`

  * :web:`research.tuni.fi/system-on-chip/tools <research.tuni.fi/system-on-chip/tools/>`
  * :web:`gitter.im/hdl/community?at=6132117a5b92082de1807f54 <gitter.im/hdl/community?at=6132117a5b92082de1807f54>`:
    *"I also worked together with the Kactus2 devs and had monthly meeting for a few years to push that as the preferred
    solution and I've been periodically trying to build a reference design that uses Kactus2+FuseSoC"*.

* :web:`olofkindgren.blogspot.com: IP-XACT: The good, the bad and the outright madness <olofkindgren.blogspot.com/2016/11/ip-xact-good-bad-and-outright-madness.html>`
* :web:`youtube.com: ORPSoCv3 - OpenRISC Project Meeting 2012 <www.youtube.com/watch?v=vYJjIoV0G3U>`
* :gh:`fvutils/ivpm`
