#!/bin/bash 

# converts mp3s to wavs with the required encoding

for i in ./*.mp3
 do sox -S "$i" -r 8k -b 16 -c 1 -e signed-integer "$(basename -s .mp3 "$i").wav";
done;
