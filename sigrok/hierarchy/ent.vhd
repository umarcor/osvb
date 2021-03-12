library ieee;
use ieee.std_logic_1164.all;

entity ent is
  port (
    clk: in std_logic
  );
end entity;

architecture arch of ent is
  signal n_clk : std_logic;
begin
  n_clk <= not clk;
end architecture;
