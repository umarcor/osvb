"""
Verify that all the tests work
"""

import sys
from sys import executable, platform
from pathlib import Path
from subprocess import check_call, STDOUT
from shutil import which
import unittest
import pytest


isWin = platform == 'win32'


class TestExtended(unittest.TestCase):
    """
    Verify that all the tests work
    """

    def setUp(self):
        self.shell = [which('bash')] if platform == 'win32' else []
        self.root = Path(__file__).parent
        print('\n::group::Log')
        sys.stdout.flush()

    def tearDown(self):
        print('\n::endgroup::')
        sys.stdout.flush()


    def _sh(self, args):
        check_call(self.shell + args, stderr=STDOUT)

    def _tcl(self, args):
        check_call(['tclsh'] + args, stderr=STDOUT)

    def _py(self, args):
        check_call([executable] + args, stderr=STDOUT)


    def test_AXI4Stream_VUnit(self):
        self._py([str(self.root / 'AXI4Stream' / 'test' / 'vunit' / 'run.py')])

    def test_AXI4Stream_VUnitCAPI(self):
        self._py([str(self.root / 'AXI4Stream' / 'test' / 'vunit' / 'run_capi.py')])

    @pytest.mark.xfail
    def test_AXI4Stream_OSVVM_TCL(self):
        self._tcl([str(self.root / 'AXI4Stream' / 'test' / 'osvvm' / 'run.pro')])

    @pytest.mark.xfail
    def test_AXI4Stream_OSVVM_VUnit(self):
        self._py([str(self.root / 'AXI4Stream' / 'test' / 'osvvm' / 'run.py')])

    @pytest.mark.xfail
    def test_SFF_VUnit_cocotb(self):
        self._py([str(self.root / 'SFF' / 'test' / 'run.py'), '-v'])
