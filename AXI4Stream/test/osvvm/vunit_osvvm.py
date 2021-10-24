# Proof of concept of a helper function to add OSVVM and/or OSVVMLibraries to a VUnit project (to be tested with GHDL)


def osvvm_filter_files(path):
    # Can't compile all OSVVM files since some depend on simulator
    # This naive filter compiles everything except Aldec and Cadence related files
    return [
        file
        for file in path.glob("*.vhd")
        if (not str(file).endswith("_c.vhd") and not str(file).endswith("_Aldec.vhd"))
    ]


def add_osvvmlibs(
    VUnitProject,
    Sources,
    NoCore=False,
    NoLibs=False,
    Version=None
):
    if Version is not None:
        print("[add_osvvmlibs] Option 'Version' not implemented yet!")
        # TODO check if 'Sources' is a submodule, and ensure that it is at tag 'Version'.
        #["git", "checkout", "-b", f"v{Version}", Version]
        #["git", "submodule", "update", "--init", "--recursive"]

    if not NoCore:
        VUnitProject.add_library("OSVVM").add_source_files(osvvm_filter_files(Sources / "osvvm"))

    if not NoLibs:
        VUnitProject.add_library("OSVVM_Common").add_source_files(Sources / "Common/src/*.vhd")
        VUnitProject.add_library("OSVVM_AXI4").add_source_files(
            [Sources / f"AXI4/{subdir}/src/*.vhd" for subdir in ["common", "AxiStream", "Axi4"]]
        )
