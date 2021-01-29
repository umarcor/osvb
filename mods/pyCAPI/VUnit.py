# Python API for using CAPI 3 core files from VUnit

def AddCoreFilesets(
    vunitHandle,
    core,
    filesets
):
    """
    Add the sources of some filesets from a CAPI 3 compliant core, into a VUnit
    handle through VUnit's API (``add_library`` and ``add_source_files``).

    :param vunitHandle: handle to the VUnit object instance.
    :param core: CAPI 3 compliant object (coming from LoadCoreFile).
    :param filesets: name of the filesets to be added into the VUnit handle.
    """
    _root = core.FILE_PATH.parent

    _defaultLib = 'VUnitUserLib'
    _sources = { _defaultLib: [] }

    for fsetname in filesets:
        if fsetname in core.filesets:
            fset = core.filesets[fsetname]
            _lib = _defaultLib if fset.logical_name == '' else fset.logical_name
            if _lib not in _sources:
                _sources[_lib] = []
            _sources[_lib] += [_root / fset.path / fstr for fstr in fset.files]

    for _lib, _files in _sources.items():
        vunitHandle.add_library(_lib).add_source_files(_files)
