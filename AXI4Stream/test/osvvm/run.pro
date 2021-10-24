cd [file dirname $argv0]

set OSVVMLibraries ../../../mods/osvvm

source $OSVVMLibraries/Scripts/StartUp.tcl

build $OSVVMLibraries/osvvm/osvvm.pro
build $OSVVMLibraries/Common/Common.pro
build $OSVVMLibraries/UART/UART.pro
build $OSVVMLibraries/AXI4/common/common.pro
build $OSVVMLibraries/AXI4/AxiStream/AxiStream.pro
build $OSVVMLibraries/AXI4/Axi4Lite/Axi4Lite.pro
build $OSVVMLibraries/AXI4/Axi4/Axi4.pro

build $OSVVMLibraries/UART/testbench/testbench.pro
build $OSVVMLibraries/AXI4/AxiStream/testbench_ghdl/testbench_ghdl.pro

build ./testbench.pro
