#!/usr/bin/env sh

set -e

cd $(dirname "$0")

if [ ! $(which time) ]; then
  echo "Package 'time' is required!"
  exit 1
fi

cd resolution/waves
mkdir -p ../logs
for FILE in \
  wave_auto_us.vcd \
  wave_auto_ns.vcd \
  wave_auto_ms.vcd \
  wave-nodate_auto_ns.vcd \
  wave-nodate_auto_us.vcd \
  wave-nodate_auto_ms.vcd \
  wave_ms_ms.vcd \
  wave_us_us.vcd \
  wave_ns_ns.vcd \
  wave_us_ms.vcd \
  wave_ns_us.vcd \
  wave-nodate_ms_ms.vcd \
  wave-nodate_us_us.vcd \
  wave-nodate_ns_ns.vcd \
  wave-nodate_us_ms.vcd \
  wave-nodate_ns_us.vcd \
; do
  printf "\n> sigrok-cli -I vcd -i - < resolution/$FILE\n"
  $(which time) -v sigrok-cli -I vcd -i - > ../logs/"$FILE".log < "$FILE"
done

#wave_ns_ms.vcd \
#wave_ps_ns.vcd \
#wave_ps_us.vcd \
#wave_ps_ms.vcd \

#wave-nodate_ns_ms.vcd \
#wave-nodate_ps_ns.vcd \
#wave-nodate_ps_us.vcd \
#wave-nodate_ps_ms.vcd \
#wave_ns.vcd \
#wave_us.vcd \
#wave_ms.vcd \
#wave-nodate_ns.vcd \
#wave-nodate_us.vcd \
#wave-nodate_ms.vcd \

cd ../../hierarchy
printf "\n> sigrok-cli -I vcd -i - > wave.log < hierarchy/wave.vcd\n"
sigrok-cli -I vcd -i - > wave.log < wave.vcd

#sigrok-cli -I vcd:downsample=1000000 -i -
#-O ascii
