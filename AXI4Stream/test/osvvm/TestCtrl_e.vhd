-- This source is based on:
-- 'AxiStream/testbench/TestCtrl_e.vhd' from OSVVM/AXI4 (Apache License, Version 2.0)

library ieee ;
  use ieee.std_logic_1164.all ;
  use ieee.numeric_std.all ;
  use ieee.numeric_std_unsigned.all ;

library OSVVM ;
  context OSVVM.OsvvmContext ;

library osvvm_AXI4 ;
    context osvvm_AXI4.AxiStreamContext ;

entity TestCtrl is
  generic (
    ID_LEN   : integer ;
    DEST_LEN : integer ;
    USER_LEN : integer
  ) ;
  port (
      -- Global Signal Interface
      nReset      : In    std_logic ;
      -- Transaction Interfaces
      StreamTxRec : InOut StreamRecType ;
      StreamRxRec : InOut StreamRecType

  ) ;

  -- Derive AXI interface properties from the StreamTxRec
  constant DATA_WIDTH : integer := StreamTxRec.DataToModel'length ;
  constant DATA_BYTES : integer := DATA_WIDTH/8 ;

  -- Access Burst FIFOs in Axi4Master using external names
  alias TxBurstFifo is <<variable ^.Transmitter_1.BurstFifo : osvvm.ScoreboardPkg_slv.ScoreboardPType>> ;
  alias RxBurstFifo is <<variable ^.Receiver_1.BurstFifo : osvvm.ScoreboardPkg_slv.ScoreboardPType>> ;

end entity TestCtrl ;
