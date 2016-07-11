#!/bin/bash
#Killing all applications on device

while read line;
do

   # echo "Killing app $line"
  if [[ ${line:0:1} != '#' ]]; then
    echo "stopping $line"
    adb shell am force-stop $line
  fi
done < "$1"
