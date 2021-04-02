.. _OSVB:API:Logging:

Logging
#######

Unarguably, the most relevant feature of a testing/verification ecosystem is a robust solution for reporting test results
and for providing feedback to the users. Since most executions are to be run unattended, spotting regressions needs to be
reliable and must provide a quick procedure for reproducing issues locally. Therefore, logging features are tightly
related to :ref:`OSVB:API:Tool` and :ref:`OSVB:API:Runner`.

Terminal
========

In the terminal, VUnit provides a coloured summary of the tests and the results at the end of the execution of a ``run.py`` script.
By default, logging is saved to files and not shown in the terminal. However, CLI option ``-v`` allows printing the content.
Moreover, VUnit's VHDL library ``logging`` allows using custom loggers with fine grained control of the scope and the consumers
(CSV files and/or display/screen).

.. figure:: http://vunit.github.io/_images/vunit_demo.gif
  :alt: Interactive VUnit session
  :width: 600px
  :align: center

  An interactive VUnit session.

Nonetheless, in complex projects, users do typically handle several run scripts, for testing different units/modules of the
designs. The recommended approach for those cases is using `pytest <https://docs.pytest.org/>`__, a framework
built on top of the built-in :py:mod:`unittest` unit testing framework in Python. Similarly to VUnit, pytest provides
automatic discovery, marks and hooks for fine grained control of test execution.

*TBC*

* *OSVVM's logging features*.
* *pyIPCMI's vendor log processor*.

Waveforms
=========

*TBC*

* *TCL plumbing for automatic/interactive waveform loading/saving*.
* *Post-processing of waveforms*:

  * :ref:`OSVB:Notebook:fpconv`
  * :ref:`OSVB:Notebook:sigrok`

xUnit/UCDB
==========

VUnit has built-in support for generating `xUnit <https://en.wikipedia.org/wiki/XUnit>`__ (XML) reports. In fact,
VUnit's name comes from *VHDL unit testing framework* (see `Wikipedia: List of unit testing frameworks <https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks>`__).
CLI option ``-x`` allows specifying the target file name. Two different formats are supported: `Jenkins <https://www.jenkins.io/>`__
(`JUnit <https://plugins.jenkins.io/junit/>`__) and `Bamboo <https://www.atlassian.com/software/bamboo>`__. JUnit is
also supported on GitLab CI: `docs.gitlab.com: Unit test reports <https://docs.gitlab.com/ee/ci/unit_test_reports.html>`__.
Python's unittest (and, therefore, pytest) was originally inspired by JUnit, so it has a similar flavor as unit testing
frameworks in other languages.

Therefore, by using VUnit's simulator interface and test runner infrastructure, it is already possible to generate fine
grained reports in a standard format. This might be useful for users of OSVVM and/or UVVM, which don't have an
equivalent feature.

Cocotb can also generate xUnit reports, independently from VUnit. See `docs.cocotb.org: COCOTB_RESULTS_FILE <https://docs.cocotb.org/en/stable/building.html?highlight=xunit#envvar-COCOTB_RESULTS_FILE>`__.
Precisely, this is related to the duplicated test/regression management features in both frameworks. At the moment, users are
expected to handle them independently when mixed (HDL + cocotb) testsuites are run. However, there is work in progress for
hopefully unifying them automatically (through some post-simulation helper hook).

Unified Coverage Database (UCDB)
--------------------------------

The main constraint for displaying combined results of multiple HDL tests is that xUnit is expected to have a single
level of hierarchy (suites and tests). Yet, typically, different types of results can be produced when testing HDL
designs (unit tests, assertions, coverage, etc.). Therefore, some mechanism needs to be added for allowing at least one
additional hierarchy level. That might be an additional field in the XML, or prepending suite names with specific
keywords.

Alternatively, Unified Coverage Database (UCDB) is one of the components of the Unified Coverage Interoperability
Standard (UCIS) developed by Accellera, Mentor Graphics and Cadence. The UCDB is used by Siemens' tools for tracking
results, and they have a GUI module for browsing them. At first sight, UCDB/UCIS are complex and not easy to work with,
however, most of the potential result types are already covered by the specification (see `Unified Coverage Interoperability Standard Version <https://www.accellera.org/downloads/standards/ucis>`__
and `OSVVM Forums: Cover group and Mentor UCDB <https://osvvm.org/forums/topic/cover-group-and-mentor-ucdb>`__).
Fortunately, there is an open source Python package that provides an API to UCIS data (`fvutils/pyucis <https://github.com/fvutils/pyucis>`__)
as well as an open source Qt based GUI (`fvutils/pyucis-viewer <https://github.com/fvutils/pyucis-viewer>`__).

Hence, it might be possible to dump results from open source frameworks/methodologies/tools to UCDB for reusing
Siemens' GUI or vice versa. From an open source community perspective, it feels more sensible to dump content from UCDB
to an open source XML/JSON/YAML format specification. However, as far as we are aware, such FLOSS specification adapted
to hardware designs does not exist yet. Moreover, the most used HDL languages are neither open source. Hence, although
not ideal, using UCDB wouldn't be disruptive in this regard. Should you know about any open source alternative, or if
you represent Accelera, Siemens' and/or Cadence and want to open source UCDB/UCIS, please `let us know <https://github.com/umarcor/osvb/issues/new>`__!

Web frontend
------------

It would be interesting to have a vendor agnostic tool for visualizing either xUnit or UCDB/UCIS reports. Since XML,
JSON or YAML are used, web technologies (HTML + CSS + JavaScript) feel like a sensible choice. Generating an static page
which can be hosted on GitHub Pages or GitLab Pages allows granular analysis of CI results, while also being usable
locally. There are several simple and not-so-simple solutions available for xUnit files:

* `w3schools.com/howto/howto_js_treeview <https://www.w3schools.com/howto/howto_js_treeview.asp>`__
* `lukejpreston.github.io/xunit-viewer <https://lukejpreston.github.io/xunit-viewer/>`__
* `Standalone JUnit XML report viewer <https://softwarerecs.stackexchange.com/questions/3666/standalone-junit-xml-report-viewer>`__
