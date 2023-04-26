./wait-button.sh
ret=$?
if [ ${ret} -eq 0 ]; then
  ./shutter.sh
  ret=$?
  if [ ${ret} -eq 1 ]; then
    echo 'shutter.sh error'
    exit 1
  fi

  python s3-up.py
  ret=$?
  if [ ${ret} -eq 1 ]; then
    echo 's3-up.py error'
    exit 1
  fi

  ./line-push.sh
  ret=$?
  if [ ${ret} -eq 1 ]; then
    echo 'line-push.sh error'
    exit 1
  fi
else
  echo 'wait-button.sh error'
  exit 1
fi

#python_pid=`pgrep -f 'python -m http.server'`
#kill -9 $python_pid
#cd image
#./server.sh &
