-- This source is based on a message posted by Lars Asplund in VUnit's gitter chat room:
-- https://gitter.im/VUnit/vunit?at=600b57a6a2354e44ac9ff33d

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std_unsigned.all;

library vunit_lib;
context vunit_lib.vunit_context;
context vunit_lib.vc_context;
context vunit_lib.data_types_context;
use vunit_lib.random_pkg.all;

entity tb_axi_stream_performance is
  generic(
    runner_cfg : string
  ) ;
end entity;

architecture a of tb_axi_stream_performance is
  constant clk_period        : time := 10 ns ;
  constant data_width        : natural := 8;
  constant master_axi_stream : axi_stream_master_t := new_axi_stream_master ( data_length => data_width ) ;
  constant slave_axi_stream  : axi_stream_slave_t  := new_axi_stream_slave  ( data_length => data_width ) ;

  signal clk, rst, rstn : std_logic := '0' ;

begin

  clk <= not clk after clk_period/2;
  rstn <= not rst;

  test_runner : process
    constant n_frames : natural := 4;
    variable image : integer_vector_ptr_t := random_integer_vector_ptr(
      length => 68 * 84,
      bits_per_word => data_width,
      is_signed => false);
    variable image_copy : integer_vector_ptr_t := image;
  begin
    test_runner_setup(runner, runner_cfg);

    rst <= '1';
    wait for 15*clk_period;
    rst <= '0';

    if run("Test startup/teardown overhead") then
      null;

    elsif run("Test push performance") then
      for frame in 1 to n_frames loop
        for i in 0 to length(image) - 1 loop
          push_axi_stream(net, master_axi_stream, to_slv(get(image, i), data_width));
        end loop;
      end loop;

    elsif run("Test push/pop performance") then
      for frame in 1 to n_frames loop
        for i in 0 to length(image) - 1 loop
          push_axi_stream(net, master_axi_stream, to_slv(get(image, i), data_width));
        end loop;

        for i in 0 to length(image) - 1 loop
          check_axi_stream(net, slave_axi_stream, to_slv(get(image, i), data_width));
        end loop;
      end loop;

--    elsif run("Test push/pop performance with integer_vector_ptr") then
--      for frame in 1 to n_frames loop
--        push_axi_stream(net, master_axi_stream, image);
--        image := image_copy;
--
--        for i in 0 to length(image) - 1 loop
--          check_axi_stream(net, slave_axi_stream, to_slv(get(image, i), data_width));
--        end loop;
--      end loop;

    end if;

    test_runner_cleanup(runner);
  end process;

  uut_vc: entity work.vc_axis
  generic map (
    m_axis     => master_axi_stream,
    s_axis     => slave_axi_stream,
    data_width => data_width
  )
  port map (
    clk  => clk,
    rstn => rstn
  );

end architecture;
