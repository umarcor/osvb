library ieee;
context ieee.ieee_std_context;
use ieee.math_real;

entity low is
  port (
    clk: in std_logic
  );
end entity;

architecture arch of low is
  signal n_clk : std_logic;
begin
  n_clk <= not clk;
end architecture;

----

library ieee;
context ieee.ieee_std_context;
use ieee.math_real;

entity ent is
  port (
    clk: in std_logic
  );
end entity;

architecture arch of ent is
  signal n_clk : std_logic;
  signal cnt: integer := -15;
  signal r: real := 0.0;
begin

  n_clk <= not clk;

  process(clk)
  begin
    if rising_edge(clk) then
      cnt <= cnt+1;
      r <= math_real.sqrt(real((15+cnt)/8)) + 0.75 * real(cnt);
    end if;
  end process;

  inst: entity work.low
    port map (
      clk => clk
    );

end architecture;

----

library ieee;
context ieee.ieee_std_context;

entity tb is
end entity;

architecture arch of tb is
  signal clk : std_logic := '0';
begin

  clk <= not clk after 10 ns;

  inst: entity work.ent
    port map (
      clk => clk
    );

end architecture;
