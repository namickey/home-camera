#!/bin/bash

# 起動前に、起動中のプロセスがあれば削除する。
python_pid=`pgrep -f './shutter.sh'`
kill -9 $python_pid

python_pid=`pgrep -f './move-and-s3up.sh'`
kill -9 $python_pid

# bashを抜けた後にプロセス終了しないようにnohupを付与
nohup ./shutter.sh &

nohup ./move-and-s3up.sh &
