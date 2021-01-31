.. _OSVB:Co-simulation:

Co-simulation
#############

Advanced verification strategies do typically raise the abstraction level of the workflow, bringing hardware design close
to software development. In this context, engineers have a natural trend towards using more flexible languages with vast
libraries implementing advanced domain-specific functionalities. Some of the most common non-HDL languages used verification
are C/C++ and Python.

Traditional HDL languages and most simulators support one or multiple standard or non-standard co-simulation interfaces for
runtime interaction between HDLs and software languages (typically C/C++, as a reference). Here, standard interfaces are
summarized.

.. IMPORTANT::
  Licensing constraints of many vendor tools do not allow discussing features and/or perfomance publicly. Therefore, this
  section contains references to interfaces supported by open source tools only, which don't have such knowledge limitations.

VPI
===

Verilog Procedural Interface (VPI) is the standard co-simulation interface in Verilog 2005. It was originally known
as PLI 2.0, because it replaced the deprecated Program Language Interface (PLI) defined in earlier versions of the language.

The usage of VPI is based on registering callbacks at specific events using the provided C API. C functions can also invoke
standard verilog system tasks. A relevant feature of this co-simulation approach is that HDL sources are unmodified. Registering
co-simulation callbacks is independent from the sources that compose the design and/or the HDL testbench.

.. NOTE::
  Non-intuitively, GHDL implements VPI for interacting with VHDL sources. Back in 2000-2008, there was no standard interface
  available for VHDL, so the author of GHDL implemented VPI for allowing co-simulation.

DPI
===

Direct Programming Interface (DPI) is an standard co-simulation interface defined in System Verilog. It is mainly meant for
co-simulation with C, C++ or SystemC. However, unlike VPI, setting up a DPI co-simulation consists of two layers. On the one
hand, the resources to be used with foreign languages are explicitly declared in the System Verilog sources. On the other hand,
sources in a foreign language provide the complementary bodies that match the prototypes of the resources declared in the first
layer. In other words, DPI allows users/developers to define custom APIs between System Verilog and foreign languages that
understand C/C++ semantics.

VHPI
====

VHDL Procedural Interface (VHPI) is the standard co-simulation interface in VHDL 2008 and VHDL 2019. It is heavily inspired
on VPI, so the workflow/usage is equivalent: a C/C++ API allows registering callbacks and models, without modifying HDL sources.

The definition and descriptions of VHPI are software-centric, i.e. mostly meant for complex software tool developers having
access to the full HDL hierarchy from an advanced software API. It is, therefore, a very powerful API with a very steep learning
curve. As a result, adoption by vendors has been slow and uneven. At the same time, there was not a critical mass of VHDL use
cases, and the apparent lack of interest from users didn't push vendors further.

VFFI/VDPI
=========

Back in 2005-2006, the author of GHDL implemented a co-simulation feature named VHPIDIRECT. It is, essentially, a Foreign
Function Interface (FFI) for executing foreign subprograms from VHDL. Function/procedure prototypes are declared in VHDL with
an specific ``FOREIGN`` attribute. Matching foreign (C/C++) bodies can be provided through pre-built shared libraries and/or
as C sources/objects to be used during elaboration/linking.

The implementation of VHPIDIRECT in GHDL was inspired on some draft of VHPI, which was apparently modified before making it
into the VHDL 2008 standard. As a result, although the VHPIDIRECT is used/defined in the LRM, GHDL's implementation is not
compliant. Precisely, the standard requires some specific intermediate structs (fat pointers) to be used between VHDL and
the foreign langauge; however, GHDL's implementation passes arguments directly (by value or by reference).

It is rather obvious that System Verilog's DPI resembles GHDL's VHPIDIRECT just as much as VHPI was inpired by VPI. In 2011,
a Language Change Specification (LCS) proposal was submitted for VHDL 201X to support a DPI. It didn't make it due to the
workload in the VHDL Analysis and Standardization Group (VASG). However, since Q2 2020, the VASG is working on gathering
and updating a proposal for standardizing an interface named VHDL Foreign Function Interface (VFFI) or VHDL Direct Programming
Interface (VDPI), which formalizes the direct implementation available in GHDL and makes it generic enough for any vendor.

* `gitlab.com/IEEE-P1076/VHDL-Issues: Direct Programming Interface (DPI) | Foreign Function Interface (FFI) <https://gitlab.com/IEEE-P1076/VHDL-Issues/-/issues/10>`__
