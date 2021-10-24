# Authors:
#   Unai Martinez-Corral
#
# Copyright 2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


"""
Verify that all the tests work
"""

from sys import stdout as sys_stdout
from sys import executable, platform
from pathlib import Path
from subprocess import check_call, STDOUT
from shutil import which
import unittest
from pytest import mark


isWin = platform == "win32"


class TestExtended(unittest.TestCase):
    """
    Verify that all the tests work
    """

    def setUp(self):
        self.shell = [which("bash")] if platform == "win32" else []
        self.root = Path(__file__).parent
        print("\n::group::Log")
        sys_stdout.flush()

    def tearDown(self):
        print("\n::endgroup::")
        sys_stdout.flush()

    def _sh(self, args):
        check_call(self.shell + args, stderr=STDOUT)

    def _tcl(self, args):
        check_call(["tclsh"] + args, stderr=STDOUT)

    def _py(self, args):
        check_call([executable] + args, stderr=STDOUT)

    # AXI4Stream

    def test_AXI4Stream_VUnit(self):
        self._py([str(self.root / "AXI4Stream/test/vunit/run.py")])

    def test_AXI4Stream_VUnitCAPI(self):
        self._py([str(self.root / "AXI4Stream/test/vunit/run_capi.py")])

    @mark.xfail
    def test_AXI4Stream_OSVVM_TCL(self):
        self._tcl([str(self.root / "AXI4Stream/test/osvvm/run.pro")])

    @mark.xfail
    def test_AXI4Stream_OSVVM_VUnit(self):
        self._py([str(self.root / "AXI4Stream/test/osvvm/run.py")])

    # SFF

    @mark.xfail
    def test_SFF_VUnit_cocotb(self):
        self._py([str(self.root / "SFF/test/run.py"), "-v"])
