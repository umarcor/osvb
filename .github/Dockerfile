FROM ghdl/vunit:llvm-master

COPY . /tmp/cocotb

RUN apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    g++ \
    python3-dev \
 && apt-get autoclean && apt-get clean && apt-get -y autoremove \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install -U /tmp/cocotb --progress-bar off
