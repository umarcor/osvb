cd [file dirname $argv0]

set OSVVMLibraries ../../../mods/osvvm

source $OSVVMLibraries/Scripts/StartUp.tcl
build $OSVVMLibraries/OsvvmLibraries.pro

library osvvm_TbAxiStream
analyze TestCtrl_e.vhd
analyze TbStream.vhd
analyze TbStream_SendGet1.vhd
simulate TbStream_SendGet1
