import cocotb
from cocotb.triggers import Timer, RisingEdge


@cocotb.test()
async def test_nothing(dut):
    pass  # tests nothing and returns immediately

    # since no exceptions were thrown, the test is counted as a PASS


@cocotb.test()
async def test(dut):

    # we need to define a clock process to run concurrently

    # define the clock process
    async def clock():
        # write initial value
        dut.c.value = 0
        while True:
            # wait half period
            await Timer(5, 'ns')
            # invert and write back
            dut.c.value = ~int(dut.c.value)

    # run it concurrently
    cocotb.fork(clock())

    # for future reference, the above is available as cocotb.clock.Clock
    # most examples and user code uses `Clock`

    # make some data to test with
    data = list(range(10))

    # we need to be able to stimulate the FF input and check the FF output at the same time
    # so we will need them them run concurrently.

    # define the stimulus
    async def stimulus():
        for d in data:
            # synchronize on a clock edge
            await RisingEdge(dut.c)
            # write out the next data
            dut.d.value = d

    # run the stimulus concurrently
    cocotb.fork(stimulus())

    # we will just do the check process inline, in the current process,
    # so we don't have to define another process

    # skip the first clock, this is when data is first bewing written to the input
    # so we won't see it until the next clock edge
    await RisingEdge(dut.c)

    for d in data:
        # synchronize on the clock
        await RisingEdge(dut.c)
        # assert the value is what we expect
        assert dut.q.value == d
