# Python Data Model for CAPI 3 core files

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


from typing import Dict, List, Union
from pathlib import Path
from dataclasses import dataclass, field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class IpCoreConfig(YamlDataClassConfig):
    """
    Each core file must contain an 'ipcore' field with the metadata of the design.
    """

    namespace: str = None
    name: str = None
    version: str = None


@dataclass
class FilesetConfig(YamlDataClassConfig):
    """
    A Fileset is a group of sources of the same type, to be used together.
    """

    path: str = field(default_factory=str)
    file_type: str = field(default_factory=str)
    logical_name: str = field(default_factory=str)
    files: List[str] = None


@dataclass
class Config(YamlDataClassConfig):
    """
    Definition of the CAPI 3 format for core configuration files.
    """

    CAPI: int = None

    ipcore: IpCoreConfig = None

    # TODO Should be a Union for supporting a global 'file_type'
    # filesets: Dict[str, Union[str, FilesetConfig]] = None
    filesets: Dict[str, FilesetConfig] = None


def LoadCoreFile(coreFilePath):
    """
    Load a CAPI 3 compliant core configuration file and unmarshal it.

    :param coreFilePath: location of the ``*.core`` file to be loaded.
    """
    _cpath = Path(coreFilePath)
    _core = Config()
    _core.load(_cpath)
    _core.FILE_PATH = _cpath
    print(_core.FILE_PATH)
    print("CAPI:", _core.CAPI)
    print("IpCore:")
    print("  namespace:", _core.ipcore.namespace)
    print("  name:", _core.ipcore.name)
    print("  version:", _core.ipcore.version)
    print("Filesets:")
    for key, val in _core.filesets.items():
        print(" - %s:" % key)
        print("   path:", val.path)
        print("   file_type:", val.file_type)
        print("   logical_name:", val.logical_name)
        print("   files:", val.files)

    return _core
