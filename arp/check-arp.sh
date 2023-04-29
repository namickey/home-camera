#!/bin/bash

nowdate=`date "+%Y%m%d %H:%M:%S"`
sudo arp-scan 192.168.1.1/24 | grep 192.168 | grep -v Interface | sort | sed -e "s/^/$nowdate /g" > tmp.txt
cat tmp.txt >> arp.txt

num=$(cat tmp.txt | grep ${waka_mac} | wc -l)
if [[ ${num} -ne "0" ]]; then
  ./counter-push.sh
else
  ./counter-no-push.sh
fi
