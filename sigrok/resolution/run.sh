#!/usr/bin/env sh

set -e

cd $(dirname "$0")

run_sim () {
  echo "run_sim: $@"

  arch="$1"
  name="$1"

  unset timeres
  if [ -n "$2" ]; then
    timeres="--time-resolution=$2"
    name="${2}_${arch}"
  fi

  echo "> Analyze tb_${arch}.vhd ($timeres)"
  ghdl -a $timeres tb_"$arch".vhd

  for args in \
    "--vcd=waves/wave_${name}.vcd" \
    "--vcd=waves/wave-nodate_${name}.vcd --vcd-nodate" \
    "--vcdgz=waves/wave_${name}.vcdgz --fst=waves/wave_${name}.fst --wave=waves/wave_${name}.ghw";
  do
    ghdl -e tb

    echo " > Run $args"
    ghdl -r $timeres tb --stop-time=5ms $args
  done;
  rm *.cf
}

mkdir -p waves

if ! ghdl --help -a | grep -q time-resolution; then
  echo "option --time-resolution not available"
  for arch in ns us ms; do
    run_sim "$arch"
  done;
else
  for arch in ns us ms; do
    run_sim "$arch" auto
    run_sim "$arch" ps
    run_sim "$arch" ns
  done;

  run_sim us us
  run_sim ms us

  run_sim ms ms
fi

echo "> List waves"
ls -lah waves/wave*
