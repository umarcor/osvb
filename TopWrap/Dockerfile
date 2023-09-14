FROM ghcr.io/hdl/sim/osvb@sha256:ca08fcc7906bd34108f9bc9ef9d981045e65b09cc4961a5d271468888cfea7dc

ENV PYTHONPATH=/wrk/mods

RUN apt update -qq && apt install -y \
  g++ \
  git \
  make \
  python3-pip \
  python3-setuptools \
  antlr4 \
  libantlr4-runtime-dev \
  yosys \
 && pip3 install git+https://github.com/ghdl/ghdl.git@`ghdl version hash`
