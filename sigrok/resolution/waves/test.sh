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

for FILE in wave*.vcd; do
if [ ! $(echo "$FILE" | grep ms) ]; then
  if [ ! $(echo "$FILE" | grep us) ]; then
    printf "\n> sigrok-cli -I vcd -i - < resolution/$FILE\n"
    #$(which time) -v sigrok-cli -I vcd -i - > ../logs/"$FILE".log < "$FILE"
  fi
fi
done