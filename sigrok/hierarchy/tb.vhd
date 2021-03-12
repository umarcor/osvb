library ieee;
use ieee.std_logic_1164.all;

entity tb is
end entity;

architecture arch of tb is
  constant clk_period : time := 20 ns;
  signal clk : std_logic;
begin
  process
  begin
    clk <= '0'; wait for clk_period/2;
    clk <= '1'; wait for clk_period/2;
  end process;

  inst: entity work.ent
    port map (
      clk => clk
    );
end architecture;
