-- Authors:
--   Unai Martinez-Corral
--
-- Copyright 2020-2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--
-- SPDX-License-Identifier: Apache-2.0

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
