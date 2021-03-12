for FILE in wave*.vcd; do
if [ ! $(echo "$FILE" | grep ms) ]; then
  if [ ! $(echo "$FILE" | grep us) ]; then
    printf "\n> sigrok-cli -I vcd -i - < resolution/$FILE\n"
    #$(which time) -v sigrok-cli -I vcd -i - > ../logs/"$FILE".log < "$FILE"
  fi
fi
done