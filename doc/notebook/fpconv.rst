.. _OSVB:Notebook:fpconv:

Fixed-point conversion
######################

This section contains notes about data type exploration and visualization in arithmetic algorithms/circuits. Approaches based on HDL and programming languages are discussed.

Porting algorithms involving intensive arithmetic pipelines/sequences from a high-level software language to a Hardware Description Language (HDL) is non-trivial. On the one hand, data storage and movement need to be redesigned, in order to make the most of available resources on the target devices. On the other hand, reducing area and power constraints by using custom precision fixed-point data types is a usual strategy.

Traditionally, data type analysis and modeling is done in software. A typical procedure is to:

1.  Write an algorithm with double precision.
2.  Change to single, and compare.
3.  Do analytical analysis of propagation of error, if possible; otherwise, do experimental analysis.
4.  Change to custom fixed-point types using some library, and compare.
5.  Write/generate (V)HDL with `std_logic_vector`, `unsigned` and/or `signed`, and compare.

Multiple tools/frameworks/languages provide features for modelling fixed-point data types in step 4 (e.g. `rig <https://rig.readthedocs.io/en/stable/ten_lines/type_casts_doctest.html>`__ on `Python <https://www.python.org/>`__, `fixed_point_format <https://octave.sourceforge.io/octave/function/fixed_point_format.html>`__ on `Octave <https://www.gnu.org/software/octave/>`__, or `fixed <https://docs.rs/fixed/0.4.4/fixed/>`__ on `Rust <https://www.rust-lang.org>`__, or `shopspring/decimal <https://github.com/shopspring/decimal>`__ on `golang <https://golang.org/>`__). However, none of the mentioned resources was originally designed for modelling fixed-point circuits, even less *custom* types. Furthermore, the structure/layout of software sources can be significantly different from hardware description sources. As a result, users/developers need to duplicate the effort for avoiding mismatches between simulation models and circuit descriptions.

Several HDL generation tools avoid effort duplication by *allowing* developers not to write HDL (step 5). This is the case of `Xilinx <https://www.xilinx.com>`__'s `Vivado HLS <https://www.xilinx.com/products/design-tools/vivado/integration/esl-design.html>`__ and `Vitis <https://www.xilinx.com/products/design-tools/vitis.html>`__, `MyHDL <http://www.myhdl.org/>`__ or `migen <https://m-labs.hk/gateware/migen/>`__, among others. For example, `MathWorks <https://www.mathworks.com>`__' `MATLAB <https://www.mathworks.com/products/matlab.html>`__ and `Simulink <https://www.mathworks.com/products/simulink.html>`__ provide multiple features to do so:

* `mathworks.com/products/fixed-point-designer <https://mathworks.com/products/fixed-point-designer.html>`__
* https://mathworks.com/videos/data-type-exploration-and-visualization-of-signal-ranges-1506620567017.html
* `mathworks.com/help/fixedpoint <https://mathworks.com/help/fixedpoint>`__

  * `ref/numerictypescope.html <https://mathworks.com/help/fixedpoint/ref/numerictypescope.html>`__
  * `ug/configuring-blocks-with-fixed-point-output.html <https://mathworks.com/help/fixedpoint/ug/configuring-blocks-with-fixed-point-output.html>`__
  * `ug/fixed-point-conversion.html <https://mathworks.com/help/fixedpoint/ug/fixed-point-conversion.html>`__

MathWorks' is a comprehensive solution that allows users to run target functions/designs with multiple data sets and to gather statistics about the value of each variable (step 3). Then, it suggests lower precision datatypes automatically. It allows to customize them and to test them iteratively (step 4). Custom data types or arbitrary sizes and with various encondings are supported (see `fimath <https://es.mathworks.com/help/fixedpoint/ref/embedded.fimath.html>`__). Overall, it's a very effective solution when used along with `Coder <https://www.mathworks.com/products/matlab-coder.html>`__ and/or `HDL Coder <https://www.mathworks.com/products/hdl-coder.html>`__ (step 5).

However, using higher-level HDL generators comes with its own caveats, such as being constrained by unidiomatic constructs or not being able to customize/optimize lower level details. Users familiar with VHDL (or who are otherwise targeting FPGA or ASIC designs) might find using VHDL early in the algorithmic refinement process to be a suitable alternative. VHDL's strong type system (inherited from Ada) and the inherent concurrency in the language provide powerful features for building complex models.

Since VHDL 2008, IEEE libraries (distributed along with the IEEE 1076 standard) include generic fixed-point and floating-point packages that allow to define custom data types and rounding/truncation/resizing strategies. Furthermore, since December 2019 those libraries are open source: `opensource.ieee.org/vasg/Packages <https://opensource.ieee.org/vasg/Packages>`__. For backwards compatibility, the original proponent's (David W. Bishop's) VHDL 1993 versions are available at `FPHDL/fphdl <https://github.com/FPHDL/fphdl>`__.

Performance-wise, simulation of VHDL designs can be significantly slower than executing other (software) languages. Fortunately, `GHDL <https://github.com/ghdl/ghdl>`__ is a *libre* and *gratis* tool, which runs on multiple platforms (architectures and OSs), and allows to generate executable machine code. The generated code can be executed standalone or co-executed with sources written in a *foreign* language (see `ghdl.github.io/ghdl-cosim <https://ghdl.github.io/ghdl-cosim/>`__).

This section gathers strategies and code examples about using VHDL and GHDL for getting statistics from variables/signals in algorithms written using a higher abstraction level VHDL style (step 3). The purpose is to replace step 2 with porting the code to VHDL. Then, do steps 3 and 4 with VHDL, and rewrite step 5 as *"converting non-synthesizable sources into a synthesizable description*".

Initial code porting
********************

Although modern VHDL allows writing sources using high abstraction features, those are commonly disregarded when the language is taught, or even by practitioners. This is mostly because some (or many) of the higher level features are either not synthesizable or not supported by synthesis or simulation tools yet. Moreover, for testing and verification purposes, SystemVerilog and UVM seem to take the lead (see `larsasplund.github.io/github-facts <https://larsasplund.github.io/github-facts/>`_).

Nevertheless, many algorithms in fields such as Digital Signal Processing (DSP), image processing or machine-learning are (or can be) formulated as *basic* vector or matrix operations. These operations can be described with nested for loops and built-in operators (`+`, `-`, `*`, `/`, `**`), using a coding style similar to Ada or C. For example:

.. code-block:: vhdl

  ...
    subtype vec_t is real_vector(0 to d-1);
    type mat_t is array(0 to c-1) of vec_t;
  begin
    process
      variable m: mat_t;
      variable q: vec_t;
    begin
  ...
      for j in m'range loop
        for i in q'range loop
          q(i) := q(i) * m(j)(i) when f else q(i) + m(j)(i);
        end loop;
      end loop;
  ...


Reading/writing data to/from binary files in VHDL is also similar to other languages:

.. code-block:: vhdl

  ...
    type REAL_BIN is file of real;
    file fptr : REAL_BIN;
  begin
    process
      variable sts : FILE_OPEN_STATUS;
      variable m: mat_t;
      variable q: vec_t;
    begin
      file_open(sts, fptr, "path/to/input.bin", read_mode);
      for j in m'range loop
        for i in q'range loop
          read(fptr, m(j)(i));
        end loop;
      end loop;
      file_close(fptr);
  ...

`JSON-for-VHDL <https://github.com/Paebbels/JSON-for-VHDL>`__ is an alternative for more complex data structures.

Regarding language support, GHDL and some other commercial simulators support enough from VHDL 2008 for using generic packages and other features that facilitate code reuse. Unfortunately, most commercial simulator licenses do not allow to disclose whether features are supported. Hence, users need to check the documentation or test the features themselves.

Note that rewriting the algorithm in VHDL using `real` data type should not involve any accuracy penalty compared to the equivalent code in C or m using `double`.

Getting simulation data
***********************

After the algorithm is ported to VHDL and it is validated, analysis of error with reduced precision can be done. Sometimes, it is possible to obtain a model of propagation of error analytically. Often, an experimental approach is followed instead. Assuming availability of enough test data, the algorithm can be simulated to obtain a table that shows the specific values that each signal/variable was assigned, and how many times was each value used.

Waveform dumps
==============

Fortunately, registering all the values that each signal is assigned is a built-in feature in most HDL simulators. Precisely, waveforms are dumped to formats such as VCD or GHW. Hence, a possible approach for getting all the values that a signal was assigned is to post-process waveform dumps.

.. NOTE:: GHDL allows filtering which signals are dumped (see :option:`--read-wave-opt <ghdl.--read-wave-opt>`). This allows reducing the size of the dumps by providing the list of signals to be analyzed only.

vcd_parser
==========

`GordonMcGregor/vcd_parser <https://github.com/GordonMcGregor/vcd_parser>`__ is a VCD parser that walks through a waveform and allows to set watchers that react when named signals change. In 2018, it was forked and updated to be compatible with Python 3: `wohali/vcd_parsealyze <https://github.com/wohali/vcd_parsealyze>`__. However, neither GordonMcGregor's nor whoali's latest versions seem to handle getting values of multi-bit signals. `umarcor/vcd_parsealyze <https://github.com/umarcor/vcd_parsealyze>`__ is a fork of the latter, where reading signals of type `real` or `integer` is supported. `fpconv.py <https://github.com/umarcor/vcd_parsealyze/blob/master/examples/fpconv.py>`__ is an example that watches a clock signal and saves the values of `real` and `integer` signals at each rising edge. At the end, the table of each signal is saved to a separate tab-delimited CSV file.

Currently, reading frequency tables of `real` signals on other tools, such as MATLAB, works as expected. However, integers are dumped by GHDL as arrays of bits preprended with `b` (32 bits if negative, `<=32` bits if positive). These are not properly read by other tools yet. A future enhancement is to sign-extend them before using Python's `eval`, for convert strings to an integer.

GHDL
====

GHDL produces waveform dumps in multiple formats. Hence, its codebase contains the required logic for achieving the desired purpose. However, it is not intuitive how to get the name and value of the signals that are being dumped: `ghdl/ghdl · src/grt/grt-waves.adb#L1781-L1783 <https://github.com/ghdl/ghdl/blob/master/src/grt/grt-waves.adb#L1781-L1783>`__.

GtkWave
-------

By the same token, GtkWave contains C sources that allow reading the waveform formats generated by GHDL. However, those are not meant to be used as a toolkit (see `gtkwave/gtkwave#9 <https://github.com/gtkwave/gtkwave/issues/9>`__).

Nevertheless, showing an histogram or table of frequencies might be a handy enhancement to GtkWave's GUI featuresm, for interacting with fixed-point signals.

sigrok/PulseView
----------------

Although PulseView has some performance issues with waveforms generated by GHDL (see :ref:`OSVB:Notebook:sigrok`), the work-in-progress VCD parse module of `libsigrok <https://github.com/sigrokproject/libsigrok>`__ might have enough features for achieving the desired purpose. However, `libsigrok`'s internal structure cannot handle multi-bit signals.

.. NOTE:: The interface based on watchers and trackers of `vcd_parsealyze` is very similar to PulseView's concept of protocol analyzers.

dwfv
----

`psurply/dwfv <https://github.com/psurply/dwfv>`__ is "*a simple digital waveform viewer (in the therminal) with vi-like key binding*" written in Rust. It exposes a backend API to facilitate manipulation of signals in Rust and it provides `--stats` through the CLI interface. See `psurply/dwfv#8 <https://github.com/psurply/dwfv/issues/8>`__.

VHDL component/module
=====================

Instead of using the waveform dumping features provided by simulators, a more granular dumping of signal values is possible through a reusable VHDL component. For example:

.. code-block:: vhdl

  m_stats: entity pkg_name.stats_monitor
    generic map (
      target => "path/to/output/file"
    )
    port map (
      CLK => clk,
      DATA => (a, b, c)
    );

  a <= b + c;

The module can be implemented with multiple architectures, for generating different output formats (CSV, binary, HEX, etc.). A package can provide "dynamically sized arrays of reals" (similar to `VUnit's integer_array_pkg <https://github.com/VUnit/vunit/blob/master/vunit/vhdl/data_types/src/integer_array_pkg.vhd>`__). Alternatively, VPI/VHPI/VHPIDIRECT can be used to pass data through an access/pointer (see `ghdl.github.io/ghdl-cosim <https://ghdl.github.io/ghdl-cosim/index.html>`__) by wrapping GHDL in a foreign language.

The disadvantage of this approach is that additional VHDL code needs to be included in the sources. On the other hand, it allows to more easily decide which time frames to record and to ignore values under certain conditions.

This approach is similar to the AXI monitors that are available in `VUnit <https://github.com/VUnit>`__ or `OSVVM <https://github.com/OSVVM>`__. The difference is how the content is interpreted. In AXI monitors, the protocol is checked. In this use case, a table is filled.

Simulation/verification frameworks
==================================

cocotb uses VPI or VHPI interfaces for interacting with simulators at runtime. It allows to look/watch a hierarchical HDL path (as done in `vcd_parsealyze`). However, reading nested records and arrays in GHDL through VPI is work in progress yet (see `ghdl/ghdl#1249 <https://github.com/ghdl/ghdl/pull/1249>`__).

Analogously, MyHDL allows deriving from the `Signal` class and adding custom hooks/rules. However, MyHDL's purpose is describing circuits in Python and optionally generating HDL sources.

Analyzing simulation statistics
*******************************

The table of frequencies generated for each recorded signal can be post-processed for generating the histogram in any language with a plot/graph library (Python, Matlab, Octave, D3.js...).

Suggesting custom fixed-point formats
*************************************

Suggesting optimal word size and fractional lengths automatically is out-of-scope of this project. However, contributions of alternatives to MATLAB's `numerictypescope` that generate an interactive interface are welcome!

Regarding usage of custom types in VHDL, `FPHDL · Fixed_ug.pdf <https://github.com/FPHDL/fphdl/blob/master/Fixed_ug.pdf>`__ and `FPHDL · Float_ug.pdf <https://github.com/FPHDL/fphdl/blob/master/Float_ug.pdf>`__ are the guides of VHDL's packages for defining custom fixed/float types. Users familiar with MATLAB's `fimath` will find definition of formats/types and truncation/rounding/overflow strategies to be almost equivalent.

Converting sources into a synthesizable description
***************************************************

Apart from simulation, GHDL has experimental support for synthesis too (see :ref:`ghdl:USING:Synthesis`). Hence, after converting data types to fixed-point types (or in parallel with doing it), VHDL sources can be reshaped to properly describe the structure of the circuit. During the process, `ghdl --synth` can be used as a check. When passing, the output of GHDL (which is a VHDL 1993 netlist) can be used in vendor tools (e.g. Vivado). Alternatively, formal verification is possible through `ghdl-yosys-plugin <https://github.com/ghdl/ghdl-yosys-plugin>`__, which plugs GHDL into the open source ecosystem composed by `yosys <https://github.com/YosysHQ/yosys>`__, `nextpnr <https://github.com/YosysHQ/nextpnr>`__, `Symbiyosys <https://github.com/YosysHQ/SymbiYosys>`__, etc.

Examples
********

- `umarcor/vcd_parsealyze · examples/ghdl <https://github.com/umarcor/vcd_parsealyze/tree/master/examples/ghdl>`__ produces a VCD file to test `fpconv.py <https://github.com/umarcor/vcd_parsealyze/blob/master/examples/fpconv.py>`__.
- Example `Array and AXI4 Stream Verification Components <https://ghdl.github.io/ghdl-cosim/vhpidirect/examples/arrays.html#array-and-axi4-stream-verification-components>`__ from `ghdl.github.io/ghdl-cosim <https://ghdl.github.io/ghdl-cosim>`__ shows how to read data of type `real` (C's `double`) and convert it to/from custom signed fixed-point data types.

To Do
*****

* `smlgit/fpbinary <https://github.com/smlgit/fpbinary>`__, a binary fixed point library for Python.
* `francof2a/fxpmath <https://github.com/francof2a/fxpmath>`__, a Python library for fractional fixed-point (base 2) arithmetic and binary manipulation with Numpy compatibility.
