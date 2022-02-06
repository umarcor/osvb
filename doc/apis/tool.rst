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
artifact(s) from some HDL sources (see :web:`Hammer VLSI Flow, slide 'A Real VLSI Flow' <fires.im/micro19-slides-pdf/04_hammer_vlsi.pdf>`).
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
  shown in :ghrepo:`hdl/awesome#98 <hdl/awesome/issues/98>` might be created by visualizing the actual tasks/tools that
  people are using *in the wild*.

A task runner which allows users to compose workflows was prototyped in :ghrepo:`dbhi/run`.
There, a graphviz dot digraph is used for defining the workflows as a Directed Acyclic Graph (DAG).
Nodes can be either sources, jobs or artifacts.
The actual content of each node is defined in a sibling JSON file.
See :ghrepo:`dbhi/run: example/graph.dot <dbhi/run/blob/main/example/graph.dot>` and :ghrepo:`dbhi/run: example/config.json <dbhi/run/blob/main/example/config.json>`.
:web:`gonum <www.gonum.org/>` is used for computing the topological sort of the workflows.
Then, a CLI is provided for listing, inducing or executing.
In retrospect, picking golang for implementing the tool might have not been the best decision for a tool targeted at EDA
tooling. However, the same concepts can be applied, using already available Python libraries:

* :ghrepo:`pydoit/doit` (:web:`pydoit.org`) and :web:`Invoke <www.pyinvoke.org>`
  are Python task execution tools and libraries, which allow defining/organizing task functions from a ``.py`` file.

  * See a proof of concept for using pydoit in NEORV32: :ghrepo:`stnolting/neorv32#110 <stnolting/neorv32/pull/110>`.

* :web:`NetworkX <networkx.org>` is a network analysis library in Python, which provides graph algorithms for
  topological sorting and probably other of the features implemented in dbhi/run.
  In NetworkX "*Nodes can be 'anything'*", meaning we may have pydoit/Invoke tasks be NetworkX nodes.
  At the same time, "*edges can hold arbitrary data*", so we can have artifacts encoded in the edges, and use them
  together with source nodes.

In fact, :web:`Apache Airflow <airflow.apache.org/>` implements these concepts, and it's written in Python.
Furthermore, :web:`Google's Cloud Composer <cloud.google.com/composer>` is managed workflow orchestration service built
on Apache Airflow.
Airflow might be too specific, as it is meant for orchestrating and schduling web/remote workers in a pool, which is out
of the scope of this bundle/project.
Nonetheless, there are several shared :web:`Concepts <airflow.apache.org/docs/apache-airflow/stable/concepts.html>`
and some of their implementation decisions might be a good reference.

Moreover the design document for the reimplementation of Edalize (see :ghrepo:`Edalize (Slight return) <olofk/edalize/wiki/Edalize-(Slight-return)>`)
does also propose a similar architecture, even though terms such as directed acyclic graph or topological sorting are
not explicitly used.
Precisely, the section about :ghrepo:`Implementation <olofk/edalize/wiki/Edalize-(Slight-return)#implementation>`
proposes using EDAM as the unified format for passing parameters between nodes.

On the other hand, as shown in the diagram of section :ref:`API:Core`, developers of Edalize and PyFPGA have been
lately working towards making integration easier:

* Experimental support for *launchers* was added to Edalize (:ghrepo:`olofk/edalize@f8b3f66 <olofk/edalize/commit/f8b3f666a282e09b8ce06388101d179f8c70e8d4>`).
  That allows wrapping the lower level commands.

* :ghrepo:`OpenFlow <PyFPGA/openflow>` was split from PyFPGA.
  OpenFlow wraps (Docker/Podman) containers, allowing usage of EDA tools without installing them natively.
  By default, containers from :ghrepo:`hdl/containers` are used.

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

* :gdocs:`EDA integration: managing projects for simulation and implementation <1qThGGqSVQabts-4imn5zY5BMptp1-Q2rGiNKHDH1Pbk>`

* :gdocs:`Open Source EDA: building, packaging, installing <10_MqFjTIYVVuOJlusJydsp4KOcmrrHk03__7ME5thOI>`

* :ghrepo:`create schema for EDAM format (olofk/edalize#288) <olofk/edalize/issues/288>`

* SymbiFlow

  * :web:`SymbiFlow Publically Accessible Docs <drive.google.com/drive/folders/1euSrrszzt3Bfz792S6Ud8Ox2w7TYUZNa>`
  * :gdocs:`bit.ly/edda-conda-eda-spec: Conda based system for FPGA and ASIC Dev <1BZcSzU-ur0J02uO5FSGHdJHYGnRfr4n4Cb7PMubXOD4>`
  * :gdocs:`Next Conda Work <11XFnJ0ExBgE1pMQksw0rQerAZo3F83AVIu2YK1pbg1k>`
  * :ghrepo:`SymbiFlow/make-env`
  * :gdocs:`edalize.autosetup <1IMVrSmMO5wqTV3W22Bv2PeKtMHO3WSyCwHm3N-Wkwbk>`
  * :gdocs:`Tim's suggestions for a edalize v2 <1VakRJV0Pv4eM_hJnCCfh2l3bCMD3y07p6hFpc7z2Kg4>`
  * :gdraws:`VHDL version of "OpenTitan (and other SV designs) using open tools (for FPGAs and ASICS)" <16kKGSo84Xitmr5BiCJG3faNWt3maoKs-EHftUPDaM64>`
  * :gdraws:`SystemVerilog flows (for OpenTitan and other SV designs) using open tools (for FPGAs and ASICS) <1GEjCoLwY57bsuZoj5ymyXoToIEOC0H4j2SEYsqQupM8>`.

* :ghrepo:`cocotb[wiki]: Python Test Runner Proposal <cocotb/cocotb/wiki/Python-Test-Runner-Proposal>`.

* :ghrepo:`Highly Agile Masks Made Effortlessly from RTL (HAMMER) <ucb-bar/hammer>`.

  * HAMMER imports tools as Python classes.
    See :ghrepo:`ucb-bar/hammer: src/hammer-vlsi/README.md <ucb-bar/hammer/blob/master/src/hammer-vlsi/README.md#tool-library>`.
  * :web:`HAMMER: A Platform For Agile Physical Design [EECS-2020-28] <www2.eecs.berkeley.edu/Pubs/TechRpts/2020/EECS-2020-28.pdf>`.

* Other task execution/automation tools:

  * :ghrepo:`facebookresearch/hydra`
  * :ghrepo:`chriscardillo/gusty`
  * :ghrepo:`ray-project/ray`

    * :web:`docs.ray.io: Ray design patterns <docs.ray.io/en/master/ray-design-patterns/index.html>`

  * Not based on Python:

    * :web:`bazel.build`

      * :ghrepo:`hdl/bazel_rules_hdl`

    * :web:`cmake.org`
    * :web:`gradle.org`
    * :web:`ninja-build.org`

    * Remote execution:

      * :web:`Argo Workflows - The workflow engine for Kubernetes <argoproj.github.io/argo-workflows/>`
      * :ghrepo:`Remote Execution API <bazelbuild/remote-apis>`
      * :web:`n8n.io`

        * :ghrepo:`n8n-io/n8n`

* :ghrepo:`ktbarrett.github.io: _drafts/tool-automation.md <ktbarrett/ktbarrett.github.io/blob/master/_drafts/tool-automation.md>`

  * Find a discussion about the capabilities and limitations of pydoit in :gitter:`hdl/community?at=60f6b567926ce249e5759d03`.

* :ghrepo:`qarlosalberto/fpga-knife`

* :web:`DMTN-025: A survey of workflow management systems <dmtn-025.lsst.io>`

* :ghrepo:`fvutils/vlsim`

* `chipflow.io <https://chipflow.io/>`__

  * `ChipFlow: Technical Overview <https://indico.cern.ch/event/1071292/contributions/4535513/attachments/2322456/3955165/ChipFlow%20-%20Technical%20Overview%20%281%29.pdf>`__,
    `Microelectronics User Group Meeting, TWEPP 2021 Topical Workshop on Electronics for Particle Physics <https://indico.cern.ch/event/1071292/>`__.
