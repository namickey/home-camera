#!/bin/bash

python_pid=`pgrep -f './shutter.sh'`
kill -9 $python_pid

python_pid=`pgrep -f './move-and-s3up.sh'`
kill -9 $python_pid

nohup ./shutter.sh &

nohup ./move-and-s3up.sh &
