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

xUnit
=====

VUnit has built-in support for generating `xUnit <https://en.wikipedia.org/wiki/XUnit>`__ (XML) reports. In fact, VUnit's name
comes from VHDL unit testing framework (see `List of unit testing frameworks <https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks>`__).
CLI option ``-x`` allows specifying the target file name. Two different formats are supported: `Jenkins <https://www.jenkins.io/>`__
(`JUnit <https://plugins.jenkins.io/junit/>`__) and `Bamboo <https://www.atlassian.com/software/bamboo>`__. JUnit is also
supported on GitLab CI: `docs.gitlab.com: Unit test reports <https://docs.gitlab.com/ee/ci/unit_test_reports.html>`__. Python's
unittest (and, therefore, pytest) was originally inspired by JUnit, so it has a similar flavor as unit testing framework in other
languages.

Therefore, by using VUnit's simulator interface and test runner infrastructure, it is already possible to generate fine
grained reports in a standard format. This is specially useful for users of OSVVM and/or UVVM, which don't have an
equivalent feature.

Cocotb can also generate xUnit reports, independently from VUnit. See `docs.cocotb.org: COCOTB_RESULTS_FILE <https://docs.cocotb.org/en/stable/building.html?highlight=xunit#envvar-COCOTB_RESULTS_FILE>`__.
Precisely, this is related to the duplicated test/regression management features in both frameworks. At the moment, users are
expected to handle them independently when mixed (HDL + cocotb) testsuites are run. However, there is work in progress for
hopefully unifying them automatically (through some post-simulation helper hook).
