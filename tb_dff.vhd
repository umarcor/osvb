library ieee;
context ieee.ieee_std_context;

library vunit_lib;
context vunit_lib.vunit_context;

entity tb_dff is
  generic ( runner_cfg : string );
end entity;

architecture tb of tb_dff is

  constant clk_period : time := 20 ns;

  signal c : std_logic := '0';
  signal d, q : std_logic;

begin

  c <= not c after clk_period/2;

  main : process
  begin
    test_runner_setup(runner, runner_cfg);
    while test_suite loop
      if run("VUnit") then

        d <= '0';
        wait for clk_period;
        d <= '1';
        check_equal(q, '0');
        wait for clk_period;
        check_equal(q, '1');

      elsif run("cocotb") then

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
