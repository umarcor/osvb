.. _API:Logging:

Logging
#######

Unarguably, the most relevant feature of a testing/verification ecosystem is a robust solution for reporting test results
and for providing feedback to the users.
Since most executions are to be run unattended, spotting regressions needs to be reliable and must provide a quick
procedure for reproducing issues locally.
Therefore, logging features are tightly related to :ref:`API:Tool` and :ref:`API:Runner`.

Terminal
********

In the terminal, VUnit provides a coloured summary of the tests and the results at the end of the execution of a
``run.py`` script.
By default, logging is saved to files and not shown in the terminal.
However, CLI option ``-v`` allows printing the content.
Moreover, VUnit's VHDL library ``logging`` allows using custom loggers with fine grained control of the scope and the
consumers (CSV files and/or display/screen).

.. figure:: https://vunit.github.io/_images/vunit_demo.gif
  :alt: Interactive VUnit session
  :width: 600px
  :align: center

  An interactive VUnit session.

Nonetheless, in complex projects, users do typically handle several run scripts, for testing different units/modules of
the designs.
The recommended approach for those cases is using :web:`pytest <docs.pytest.org/>`, a framework built on top of the
built-in :py:mod:`unittest` unit testing framework in Python.
Similarly to VUnit, pytest provides automatic discovery, marks and hooks for fine grained control of test execution.

Waveforms
*********

The most widespread format for dumping waveforms is Value Change Dump (VCD), defined in the Verilog language (IEEE Std
1364-1995).
Six years later, an Extended VCD (EVCD) was defined in IEEE Std 1364-2001.
VCD is simple and compact, which allowed it to be used in fields other than Verilog simulation tools.
For instance, GHDL supports dumping VCD files.
Since VCD files are text files, some tools use VCDGZ for referring to VCD compressed using zlib/gzip.

VCD/EVCD can be read by multiple open source tools:

* :awesome:`GTKWave <gtkwave>`
* :ghrepo:`veripool/dinotrace`
* :ref:`Notebook:sigrok`
* :ghrepo:`psurply/dwfv`
* :web:`wavedrom.com`, :ghrepo:`wavedrom/vcdrom` and :ghrepo:`wavedrom/zoom`.
* :ghrepo:`Nic30/d3-wave`
* :ghrepo:`raczben/fliplot`
* :ghrepo:`lachlansneff/ligeia`
* :ghrepo:`yne/vcd`
* :ghrepo:`toem/impulse.vscode`
* :ghrepo:`bmpenuelas/hdlcomposer`
* :ghrepo:`phillbush/vcd2svg`
* :ghrepo:`Ben1152000/sootty`
* :ghrepo:`Toroid-io/vcd2wavedrom`
* :ghrepo:`cirosantilli/vcdvcd`

However, being a 20+ year old format defined for Verilog, VCD has certain limitations:

* Data cannot be accessed randomly, as it has to be sequentially parsed.
* Periodic signals are not compressed, so they take a lot of space.
* File size is huge, because it is plain text.

Anthony J. Bybell, has gathered much knowledge about alternatives through the decades he's been building and maintaining
GTKWave.
It supports FST, LXT, LXT2 and VZT formats.
See appendices C, D and F of the :web:`GTKWave User's Guide <gtkwave.sourceforge.net/gtkwave.pdf>`.
GHDL supports saving/reading waveforms as FST files, which are much smaller than VCD and they handle the same signal
types.

On the other hand, neither VCD nor FST can handle certain signal types from the VHDL language.
There is neither any equivalent in the VHDL LRM.
Tristan Gingold, author of GHDL, implemented a format named GHW for allowing all VHDL types to be dumped.
He also contributed a reader to GTKWave, which allows visualizing them.

.. NOTE::
  GTKWave provides multiple tools for converting waveforms between any of the supported formats.
  That is not trivial because some conversions are lossy or suboptimal.
  See appendix A of the :web:`GTKWave User's Guide <gtkwave.sourceforge.net/gtkwave.pdf>` and subdir
  :ghrepo:`gtkwave/gtkwave: gtkwave3-gtk3/src/helpers <gtkwave/gtkwave/tree/master/gtkwave3-gtk3/src/helpers>`.
  See also :ghrepo:`gtkwave/gtkwave#70 <gtkwave/gtkwave/issues/70>`.
  However, as far as we are aware, no other independent repository exists which is focused on providing a toolkit for
  manipulating *any* waveform programmatically.
  If GTKWave helpers are buildable/usable independently of GTKWave, it might be desirable to provide bindings in Python,
  Rust,... along with an API to the database.

Recently, Lachlan Sneff implemented Streamed Value Change Blocks (SVCB) in :ghrepo:`lachlansneff/ligeia`, a
work-in-progress "*replacement for gtkwave, written in Rust with high-performance and larger-than-memory traces in mind*".

Apart from dealing with large waveforms, there are some other formats which are used for documentation purposes:

* :ghrepo:`WaveJSON <drom/wavedrom/wiki/WaveJSON>`
* LaTeX (:web:`tikz-timing <ctan.org/pkg/tikz-timing>`)

Moreover, there are several work in progress solutions for providing TCL plumbing to allow using vendor waveform viewers
and GTKWave automatically and/or interactively:

* :ghrepo:`VUnit/vunit#690 <VUnit/vunit/pull/690>`
* :ghrepo:`VUnit/vunit#622 <VUnit/vunit/pull/622>`

With regard to post-processing of waveforms, see the following references:

* :ref:`Notebook:fpconv`
* :ghrepo:`avidan-efody/coverage`: implementation of post-process coverage, and batch waveform search.
* :glrepo:`xiretza/ghw-rs`
* :ghrepo:`Nic30/pyDigitalWaveTools`
* :ghrepo:`ics-jku/wal`
* :ghrepo:`Wren6991/asciiwave`

.. _API:Logging:OSVR:

pyEDAA.Reports
**************

See :doc:`reports:index`.
