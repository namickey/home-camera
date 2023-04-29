#!/bin/bash

num=$(cat count.txt)
if [[ $num < 1 ]]; then
  echo '0' > count.txt
else
  echo $(expr $num - 1) > count.txt
fi