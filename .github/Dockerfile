# syntax=docker/dockerfile:experimental

FROM ghdl/cosim:py AS build

RUN apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    g++ \
    python3-dev

RUN --mount=type=bind,src=.,target=/tmp/src cp -vr /tmp/src/* /tmp/ \
 && cd /tmp/cocotb \
 && python3 setup.py bdist_wheel \
 && mv dist/*.whl /tmp \
 && cd /tmp/vunit \
 && python3 setup.py bdist_wheel \
 && mv dist/*.whl /tmp \
 && cd .. \
 && rm -rf cocotb vunit

#-

FROM ghdl/cosim:py

RUN apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    libpython3.7-dev \
 && apt-get autoclean && apt-get clean && apt-get -y autoremove \
 && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,from=build,src=/tmp/,target=/tmp/ pip3 install -U /tmp/*.whl --progress-bar off \
 && rm -rf ~/.cache
