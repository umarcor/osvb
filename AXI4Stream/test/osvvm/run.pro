# Start OSVVM Tools
source  ../../OsvvmLibraries/Scripts/StartUp.tcl

# Compile all Libraries
build ../../OsvvmLibraries/osvvm/osvvm.pro
build ../../OsvvmLibraries/Common/Common.pro
build ../../OsvvmLibraries/UART/UART.pro
build ../../OsvvmLibraries/AXI4/common/common.pro
build ../../OsvvmLibraries/AXI4/AxiStream/AxiStream.pro
build ../../OsvvmLibraries/AXI4/Axi4Lite/Axi4Lite.pro
# build ../../OsvvmLibraries/AXI4/Axi4/Axi4.pro

# Run Tests
build ../../OsvvmLibraries/UART/testbench/testbench.pro
build ../../OsvvmLibraries/AXI4/AxiStream/testbench/testbench_ghdl.pro
