# Authors:
#   Unai Martinez-Corral
#
# Copyright 2020-2021 Unai Martinez-Corral <unai.martinezcorral@ehu.eus>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

FROM debian:buster AS build

RUN apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    autoconf \
    autoconf-archive \
    automake \
    ca-certificates \
    check \
    default-jdk \
    doxygen \
    git-core \
    gcc \
    g++ \
    make \
    libglib2.0-dev \
    libglibmm-2.4-dev \
    libtool \
    libusb-1.0-0-dev \
    libzip-dev \
    pkg-config \
    python3-numpy \
    python3-dev \
    python-gi-dev \
    python3-setuptools \
    swig \
 && git clone https://github.com/sigrokproject/libsigrok \
 && cd libsigrok \
 && git checkout -b pin 5bf642db \
 && ./autogen.sh \
 && ./configure \
 && make \
 && make install \
 && make DESTDIR=/tmp/sigrok install \
 && cd .. \
 && git clone https://github.com/sigrokproject/sigrok-cli \
 && cd sigrok-cli \
 && ./autogen.sh \
 && ./configure \
 && make \
 && make DESTDIR=/tmp/sigrok install

FROM debian:buster
COPY --from=build /tmp/sigrok /

RUN ldconfig /usr/local/lib \
 && apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
    libglib2.0 \
    libusb-1.0 \
    libzip4 \
    time
