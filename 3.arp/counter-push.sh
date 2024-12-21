#!/bin/bash

num=$(cat count.txt)
if [[ $num < 1 ]]; then
  ./line-push.sh
  echo '60' > count.txt
else
  echo $(expr $num - 1) > count.txt
fi