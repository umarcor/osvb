.. _OSVB:API:Runner:

Runner
######

This section covers the interface for deciding which workflows to execute, whether to run the in parallel, which
specific parameters to use and how to interpret exit/termination codes of tools, as well as gathering/buffering the
stdout/stderr and partially processing it.
Therefore, the runner API is closely related to :ref:`OSVB:API:Tool`, both of them belonging to layer 2 (Workflows) of
the :ref:`OSVB:Model`.

In the case of VUnit, the runner is composed by sibling interfaces written in Python and HDL, due to the limitations in
some older revisions of VHDL to get the termination status.

*TBC*

References
==========

* `IEEE-P1076/VHDL-Issues#13: Python API <https://gitlab.com/IEEE-P1076/VHDL-Issues/-/issues/13>`__

* `Test Anything Protocol <https://testanything.org/>`__

  * `python-tap/tappy <https://github.com/python-tap/tappy>`__: a set of tools for working with the TAP in Python.
