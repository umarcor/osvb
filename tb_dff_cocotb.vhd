library ieee;
context ieee.ieee_std_context;

library vunit_lib;
context vunit_lib.vunit_context;

entity tb_dff_cocotb is
  generic ( runner_cfg : string );
end entity;

architecture tb of tb_dff_cocotb is

  constant clk_period : time := 20 ns;

  signal c, d, q : std_logic;

begin

  main : process
  begin
    test_runner_setup(runner, runner_cfg);
    while test_suite loop
      if run("cocotb") then

        report "Test DFF (cocotb)";
        wait for 5 ms;

      end if;
    end loop;
    test_runner_cleanup(runner);
    wait;
  end process;
  test_runner_watchdog(runner, 10 ms);

  uut: entity work.dff
  port map (
    c => c,
    d => d,
    q => q
  );

end architecture;
