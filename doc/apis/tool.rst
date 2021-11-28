.. _API:Tool:

Tool
####

This section covers the interface for executing sequences of tasks (workflows) involving interaction with EDA tools.
Since each tool has different mechanisms for achieving the same results, the purpose of this interface is to provide
homogeneous wrappers that use data from :ref:`API:Project` for deciding which tasks to execute, the order, file
dependencies and artifacts.
In terms of the :ref:`EDAA:Concept`, this piece belongs to layer 2, which consumes the specific EDA interfaces in layer 1
(EDA) and layer 4 (Project).

Hardware design workflows are known for combining multiple (probably over a dozen) smaller tools for getting the desired
artifact(s) from some HDL sources (see `Hammer VLSI Flow, slide 'A Real VLSI Flow' <https://fires.im/micro19-slides-pdf/04_hammer_vlsi.pdf>`__).
Many hardware projects use traditional Makefiles or similar Python based solutions for aiding the designers.
However, most of them are meant for a given set of tasks and a limited set of predefined workflows.
Adding or customising stages requires modifying the tool, unless specific hooks are available.
That is the case with, e.g., VUnit, Edalize or PyFPGA.

Supporting multiple workflows is challenging because they are quickly changing, as new tools in the open source EDA
ecosystem get mature enough.
At the same time, users will always find creative ways for fulfilling in-house requirements and extending the workflows
with their ad-hoc software and verification infrastructure.
Therefore, we need a task management tool where workflows can be provided dynamically.
Instead of prefixed workflows, we need to define composable tasks that users can aggregate for building their paths.

For example, the following are just some of the possible workflows starting with some VHDL sources.
Each of them is subject to have some sources common/shared to others task, along with some specific sources.

* GHDL (sim)
* GHDL (sim) + cocotb
* VUnit > GHDL (sim)
* VUnit > GHDL (sim) + cocotb
* OSVVM > GHDL (sim)
* GHDL (synth) > VHDL > GHDL (sim)
* GHDL (synth) > Verilog > Verilator (sim)
* GHDL (synth) > VHDL > Vendor [&V]
* GHDL (synth) > VHDL > Verific (plugin) > Yosys [&Y]
* GHDL (synth) > Verilog > Yosys [&Y]

  * Y> JSON > nextpnr
  * Y> BLIF > VTR
  * Y> Verilog > Vendor

    * V> Xilinx Vivado
    * V> Xilinx ISE
    * V> Intel/Altera Quartus
    * V> Siemens ModelSim/QuestaSim
    * V> Aldec RivieraPRO/ActiveHDL
    * ...

.. NOTE::
  In fact, all the EDA ecosystem might be modelled using a similar approach. For execution, graphs need to be acyclic.
  However, a larger cyclic graph can be created by combining multiple DAGs. Therefore, diagrams such as the ones
  shown in `hdl/awesome#98 <https://github.com/hdl/awesome/issues/98>`__ might be created by visualizing the actual
  tasks/tools that people are using *in the wild*.

A task runner which allows users to compose workflows was prototyped in `dbhi/run <https://github.com/dbhi/run>`__.
There, a graphviz dot digraph is used for defining the workflows as a Directed Acyclic Graph (DAG).
Nodes can be either sources, jobs or artifacts.
The actual content of each node is defined in a sibling JSON file.
See `dbhi/run: example/graph.dot <https://github.com/dbhi/run/blob/main/example/graph.dot>`__ and `dbhi/run: example/config.json <https://github.com/dbhi/run/blob/main/example/config.json>`__.
`gonum <https://www.gonum.org/>`__ is used for computing the topological sort of the workflows.
Then, a CLI is provided for listing, inducing or executing.
In retrospect, picking golang for implementing the tool might have not been the best decision for a tool targeted at EDA
tooling. However, the same concepts can be applied, using already available Python libraries:

* `pydoit/doit <https://github.com/pydoit/doit>`__ (`pydoit.org <https://pydoit.org/>`__) and `Invoke <http://www.pyinvoke.org/>`__
  are Python task execution tools and libraries, which allow defining/organizing task functions from a ``.py`` file.

  * See a proof of concept for using pydoit in NEORV32: `stnolting/neorv32#110 <https://github.com/stnolting/neorv32/pull/110>`__.

* `NetworkX <https://networkx.org/>`__ is a network analysis library in Python, which provides graph algorithms for
  topological sorting and probably other of the features implemented in dbhi/run.
  In NetworkX "*Nodes can be 'anything'*", meaning we may have pydoit/Invoke tasks be NetworkX nodes.
  At the same time, "*edges can hold arbitrary data*", so we can have artifacts encoded in the edges, and use them
  together with source nodes.

In fact, `Apache Airflow <https://airflow.apache.org/>`__ implements these concepts, and it's written in Python.
Furthermore, `Google's Cloud Composer <https://cloud.google.com/composer>`__ is managed workflow orchestration service
built on Apache Airflow.
Airflow might be too specific, as it is meant for orchestrating and schduling web/remote workers in a pool, which is out
of the scope of this bundle/project.
Nonetheless, there are several shared `Concepts <https://airflow.apache.org/docs/apache-airflow/stable/concepts.html>`__
and some of their implementation decisions might be a good reference.

Moreover the design document for the reimplementation of Edalize (see `Edalize (Slight return) <https://github.com/olofk/edalize/wiki/Edalize-(Slight-return)>`__)
does also propose a similar architecture, even though terms such as directed acyclic graph or topological sorting are
not explicitly used.
Precisely, the section about `Implementation <https://github.com/olofk/edalize/wiki/Edalize-(Slight-return)#implementation>`__
proposes using EDAM as the unified format for passing parameters between nodes.

On the other hand, as shown in the diagram of section :ref:`API:Core`, developers of Edalize and PyFPGA have been
lately working towards making integration easier:

* Experimental support for *launchers* was added to Edalize (`olofk/edalize@f8b3f66 <https://github.com/olofk/edalize/commit/f8b3f666a282e09b8ce06388101d179f8c70e8d4>`__).
  That allows wrapping the lower level commands.

* `OpenFlow <https://github.com/PyFPGA/openflow>`__ was split from PyFPGA.
  OpenFlow wraps (Docker/Podman) containers, allowing usage of EDA tools without installing them natively.
  By default, containers from `hdl/containers <https://github.com/hdl/containers>`__ are used.

By combining both solutions, users can use Edalize with containers.
Anyhow, extending OpenFlow for supporting multiple and dynamically defined workflows imposes similar challenges as the
ones described for Edalize.

Even though using Python based libraries is proposed here, the architecture is not limited to Python tasks.
It is indeed desirable to reuse existing CLI or shell scripts, instead of being forced to rewrite them.
That is compulsory when dealing with vendor tools.
Furthermore, some SymbiFlow scripts for using QuickLogic devices are currently written in bash.
Therefore, having them available in the same workflow as the Python tasks makes integration easier.
In fact, both Edalize and PyFPGA are generators and wrappers around TCL scripts and/or Makefiles.

Summarising, we should agree on some common format for defining what a task is, which are the inputs and the
outputs.
That might be EDAM.
However, that is also related to pyCAPI and pyOSVR, since Source and Report nodes (aka edge payloads) should satisfy
those formats.
Therefore, we need to analyse whether those can be wrapped in EDAM.
Then, we should document how to compose and execute those tasks with pydoit/Invoke/NetworkX/Airflow;
or some custom solution if those don't fit.
From this point of view, Edalize and PyFPGA might be rethought as frontends (project managers) and backends (task
providers) of the task execution core.

References
==========

* `EDA integration: managing projects for simulation and implementation <https://docs.google.com/document/d/1qThGGqSVQabts-4imn5zY5BMptp1-Q2rGiNKHDH1Pbk>`__

* `Open Source EDA: building, packaging, installing <https://docs.google.com/document/d/10_MqFjTIYVVuOJlusJydsp4KOcmrrHk03__7ME5thOI>`__

* SymbiFlow

  * `SymbiFlow Publically Accessible Docs <https://drive.google.com/drive/folders/1euSrrszzt3Bfz792S6Ud8Ox2w7TYUZNa>`__
  * `bit.ly/edda-conda-eda-spec: Conda based system for FPGA and ASIC Dev <https://docs.google.com/document/d/1BZcSzU-ur0J02uO5FSGHdJHYGnRfr4n4Cb7PMubXOD4>`__
  * `Next Conda Work <https://docs.google.com/document/d/11XFnJ0ExBgE1pMQksw0rQerAZo3F83AVIu2YK1pbg1k>`__
  * `SymbiFlow/make-env <https://github.com/SymbiFlow/make-env>`__
  * `edalize.autosetup <https://docs.google.com/document/d/1IMVrSmMO5wqTV3W22Bv2PeKtMHO3WSyCwHm3N-Wkwbk>`__
  * `Tim's suggestions for a edalize v2 <https://docs.google.com/document/d/1VakRJV0Pv4eM_hJnCCfh2l3bCMD3y07p6hFpc7z2Kg4>`__
  * `VHDL version of "OpenTitan (and other SV designs) using open tools (for FPGAs and ASICS)" <https://docs.google.com/drawings/d/16kKGSo84Xitmr5BiCJG3faNWt3maoKs-EHftUPDaM64>`__
  * `SystemVerilog flows (for OpenTitan and other SV designs) using open tools (for FPGAs and ASICS) <https://docs.google.com/drawings/d/1GEjCoLwY57bsuZoj5ymyXoToIEOC0H4j2SEYsqQupM8>`__

* `cocotb[wiki]: Python Test Runner Proposal <https://github.com/cocotb/cocotb/wiki/Python-Test-Runner-Proposal>`__.

* `Highly Agile Masks Made Effortlessly from RTL (HAMMER) <https://github.com/ucb-bar/hammer>`__.

  * HAMMER imports tools as Python classes.
    See `ucb-bar/hammer: src/hammer-vlsi/README.md <https://github.com/ucb-bar/hammer/blob/master/src/hammer-vlsi/README.md#tool-library>`__.
  * `HAMMER: A Platform For Agile Physical Design [EECS-2020-28] <https://www2.eecs.berkeley.edu/Pubs/TechRpts/2020/EECS-2020-28.pdf>`__

* Other task execution/automation tools:

  * `facebookresearch/hydra <https://github.com/facebookresearch/hydra>`__
  * `chriscardillo/gusty <https://github.com/chriscardillo/gusty>`__
  * `ray-project/ray <https://github.com/ray-project/ray>`__

    * `docs.ray.io: Ray design patterns <https://docs.ray.io/en/master/ray-design-patterns/index.html>`__

  * Not based on Python:

    * `cmake.org <https://cmake.org/>`__
    * `gradle.org <https://gradle.org/>`__
    * `ninja-build.org <https://ninja-build.org/>`__
    * `n8n.io <https://n8n.io/>`__

      * `n8n-io/n8n <https://github.com/n8n-io/n8n>`__

* `ktbarrett.github.io: _drafts/tool-automation.md <https://github.com/ktbarrett/ktbarrett.github.io/blob/master/_drafts/tool-automation.md>`__

  * Find a discussion about the capabilities and limitations of pydoit in `gitter.im/hdl/community?at=60f6b567926ce249e5759d03 <https://gitter.im/hdl/community?at=60f6b567926ce249e5759d03>`__.

* `qarlosalberto/fpga-knife <https://github.com/qarlosalberto/fpga-knife>`__

* `DMTN-025: A survey of workflow management systems <https://dmtn-025.lsst.io/>`__

* `fvutils/vlsim <https://github.com/fvutils/vlsim>`__
