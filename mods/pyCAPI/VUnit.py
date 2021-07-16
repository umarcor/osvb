# Python API for using CAPI 3 core files from VUnit

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


def AddCoreFilesets(vunitHandle, core, filesets):
    """
    Add the sources of some filesets from a CAPI 3 compliant core, into a VUnit
    handle through VUnit's API (``add_library`` and ``add_source_files``).

    :param vunitHandle: handle to the VUnit object instance.
    :param core: CAPI 3 compliant object (coming from LoadCoreFile).
    :param filesets: name of the filesets to be added into the VUnit handle.
    """
    _root = core.FILE_PATH.parent

    _defaultLib = "VUnitUserLib"
    _sources = {_defaultLib: []}

    for fsetname in filesets:
        if fsetname in core.filesets:
            fset = core.filesets[fsetname]
            _lib = _defaultLib if fset.logical_name == "" else fset.logical_name
            if _lib not in _sources:
                _sources[_lib] = []
            _sources[_lib] += [_root / fset.path / fstr for fstr in fset.files]

    for _lib, _files in _sources.items():
        vunitHandle.add_library(_lib).add_source_files(_files)
