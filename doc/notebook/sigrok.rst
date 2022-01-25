.. _Notebook:sigrok:

sigrok-cli | Pulseview
######################

This section contains notes about reading waveforms from HDL simulators with :web:`sigrok-cli <sigrok.org/wiki/Sigrok-cli>`
and :web:`PulseView <sigrok.org/wiki/PulseView>` (see :ghrepo:`sigrokproject`).

While :ghrepo:`PulseView <sigrokproject/pulseview>` is primarily meant for data captured from real devices (logic
analyzers, oscilloscopes, multimeters, and more), some of its features can be useful for simulation and verification of
hardware description designs.
Precisely, :web:`protocol decoders <sigrok.org/wiki/Protocol_decoders>` are a nice feature to complement Verification
Components (e.g. Vunit's :web:`VCL <vunit.github.io/verification_components/user_guide.html>`), Bus Functional Models
(BFMs) and/or monitors.
Apart from vendor products, in-house custom protocol decoders can be used as a definition of the internal APIs.
Moreover, analog signal visualization can be useful to show digital words that are meant to be used as inputs to DACs.
Actually, mixed-signal cosimulations (as when combining GHDL and Xyce) produce both digital and analog traces.

The most widespread waveform format used by EDA tools is VCD: :wikipedia:`Value_change_dump`.
However, not all VHDL types can be represented in VCD files.
:awesome:`GHDL <ghdl>` supports a format named GHW, which is meant to dump traces from VHDL simulations.
Visualization of any of these types (and others) is supported by :awesome:`GtkWave <gtkwave>`.

The file format that PulseView uses internally is :web:`sigrok.org/wiki/File_format:Sigrok <sigrok.org/wiki/File_format:Sigrok>`.
Hence, any other waveform needs to be converted, and possibly filtered. Currently supported input/output formats are
listed at :web:`sigrok.org/wiki/Input_output_formats <sigrok.org/wiki/Input_output_formats>`.

Sticking to VCD, several features are (unfortunately) currently missing in :ghrepo:`libsigrok <sigrokproject/libsigrok>`
and PulseView:

* Arrays of signals, i.e. multi-bit signals, are not supported.
* Hierarchy of modules is not preserved.
* By design, signal type is `boolean` (0 or 1).
* They cannot handle huge dumps. While fast and responsive with time resolutions in the order of ms, us or ns, they have
  a hard time with ps or fs. These values are uncommon in physical capture devices, but relatively frequent in hardware
  modelling.
* Waveform formats other than VCD are not supported.

Fortunately, there is work in progress by user `gsi`, for improving and extending the VCD frontend in libsigrok. See
`wip/vcd-*` branches in :web:`repo.or.cz/libsigrok/gsi.git/refs`.

Required enhancements and possible workarounds
==============================================

Nested signal groups
--------------------

Although multi-bit signals are not supported yet, the concept of signal groups exists in PulseView. This is used to
group 1-bit signals that belong to the same interface. Currently, PulseView picks channel groups from file imports other
than VCD or from acquisition device drivers. At the same time, the VCD import frontend of libsigrok can generate nested
channel groups.
Hence, PulseView should pick up and display the groups transparently. The main remaining question is whether the
internal infrastructure of libsigrok supports nested groups.

Should nested groups be supported, three different types can be generated:

* level-0: multi-bit signals, i.e. groups of 1-bit signals that can be represented as a binary array, as an
  unsigned/signed decimal, as an hexadecimal value, etc. Moreover, any multi-bit signal can be optionally shown as an
  analog channel. This is specially useful for fixed-point types (in VHDL, `sfixed` and `ufixed`). For reference,
  GtkWave supports almost all of these features; however, displaying fixed-point values as analog channels has some
  limitations (see :ghrepo:`gtkwave/gtkwave#9 <gtkwave/gtkwave/issues/9>`).
* level-1 and above: hierarchy of the design, according to the structure of HDL sources. This is described in VCD
  through `scope module`.
* within a hierarchy level: nested groups of multi-bit signals would allow to describe interfaces such as Wishbone, AXI,
  or Avalon. Hence, protocol decoders could be written and used to display nice labels on top of them. However, this is
  typically done through naming conventions, so generation of these groups should probably be handled in PulseView and
  not in the VCD frontend.

The in-progress VCD import frontend can parse scopes and generate signal names with dot separated labels in their names.
This feature can be used to extract the hierarchy for visualization purposes.

Regarding visualization, it is currently not possible to collapse groups of multi-bit signals (not even level-0 groups).
Ideally, a collapsible tree view or anchors would be shown.

At the moment, a possible workaround for level-0 groups is to create dummy `integer` or `real` signals in the HDL design,
and convert multi-bit signals (in VHDL, `to_integer` and `to_real` can be used). However, this is not desirable, as it
requires additional coding for each signal to be visualized.

9-value logic signals
---------------------

In hardware description projects, types such as `std_logic` or `std_logic_vector` are very common. These are 9-value
enumeration types, as opposed to `boolean`. Unfortunately, sigrok and PulseView are built around `boolean` values.
Changing it is a non-trivial enhancement that might have many unexpected consequences.

The in-progress VCD import frontend converts values such as `U` to zero. This allows to import waveforms without
crashing. However, reliability of protocol decoders is doubtful in these contexts. Users should implement alternative
solutions to check the stability and strengh of signals.

Performance
-----------

Compared to GtkWave, PulseView has serious issues to handle wavefroms with small time scales. For example, the following
waveform requires several seconds to load:

.. code-block:: vcd

  $timescale
    1 ps
  $end
  $scope module tb $end
  $var reg 1 ! clk $end
  $upscope $end
  $enddefinitions $end
  #0
  0!
  #1000000000
  1!
  #2000000000
  0!
  #3000000000
  1!
  #4000000000
  0!
  #5000000000
  1!

And the following, which is the same wave with a smaller scale, produces a crash:

.. code-block:: vcd

  $timescale
    1 fs
  $end
  $scope module tb $end
  $var reg 1 ! clk $end
  $upscope $end
  $enddefinitions $end
  #0
  0!
  #1000000000000
  1!
  #2000000000000
  0!
  #3000000000000
  1!
  #4000000000000
  0!
  #5000000000000
  1!

More than 9G of RAM are used, it takes minutes to load the first ~50 us, and in the end it is frozen.

As a workaround, both libsigrok and PulseView allow downsampling when VCD files are imported. It is also possible to
*skip samples until timestamp* or to *compress idle periods*. These features should allow to avoid crashes with
simulations that last milliseconds or seconds with clock frequencies of MHz.

Moreover, GHDL's *mcode* backend allows to set the base time resolution of the simulation. See
:option:`--time-resolution <ghdl.--time-resolution>` examples in subdir :ghsrc:`sigrok/resolution <sigrok/resolution>`.

Other waveform formats
----------------------

In the wiki page about VCD, there are references to other waveform formats supported by GtkWave:
:web:`sigrok.org/wiki/File_format:Vcd <sigrok.org/wiki/File_format:Vcd>`.
However, EVCD, FST, IDX and GHW are not explicitly documented.
Hence, formats other than VCD are unlikely to be supported in libsigrok/PulseView in the near future.
In the mid-long term, it would be nice if PulseView provided a frontend compatible with GtkWave's utils/internals for
handling large waveforms.
It seems that GtkWave implements some clever memory map traversal to avoid handling the entire file in memory.

Information is available in:

* :web:`GtkWave User's Guide <gtkwave.sourceforge.net/gtkwave.pdf>` and GtkWave's codebase.
* GHDL's codebase.
* :ghrepo:`nturley/ghw-notes`.

Generating waveforms with GHDL
==============================

In this section waveform dump features of GHDL are introduced. This is a complement to the information available in the
docs: :ref:`GHDL:export_waves`.
The purpose of these examples is to provide a test suite that allows users to evaluate the features and performance of
upstream and in-progress branches.

:ghsrc:`Resolution <sigrok/resolution>`
---------------------------------------

GHDL's management of the time resolution during simulation is different depending on the backend. With LLVM or GCC, the
resolution is `1 fs`, and so is the timescale of the resulting VCD files. It cannot be modified, because the time scale
needs to be global. However, with mcode, GHDL automatically adjusts the resolution to the smallest time unit in the
design. Furthermore, CLI option :option:`--time-resolution <ghdl.--time-resolution>` allows to override it. Subdir
:ghsrc:`sigrok/resolution <sigrok/resolution>` contains three testbenches and a shell script to generate 15 waveforms
with different time resolutions (12 with mcode and 3 with LLVM). Each waveform is saved to 5 different file formats, so
75 files are generated.

======= ============== ==== ===
backend design         CLI  VCD
======= ============== ==== ===
mcode   ns             auto ns
mcode   us             auto us
mcode   ms             auto ms
mcode   ns or us or ms ps   ps
mcode   ns or us or ms ns   ns
mcode   us or ms       us   us
mcode   ms             ms   ms
LLVM    ns or us or ms      fs
======= ============== ==== ===

where:

* backend: used GHDL backend.
* design: smallest time unit in the design.
* CLI: time resolution argument.
* VCD: resulting time scale in the VCD.

:ghsrc:`Hierarchy <sigrok/hierarchy>`
-------------------------------------

libsigrok does currently not support nested name spaces (`module` keyword). This example generates a waveform from a
testbench with an instantiated entity. The waveform includes such `module` keywords. The waveform can be loaded in
PulseView without errors, but all the signals are flattened; so, the hierarchy is lost.
