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
 && ./autogen.sh \
 && ./configure \
 && make \
 && make install \
 && make DESTDIR=/tmp/sigrok install \
 && cd ..  \
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
