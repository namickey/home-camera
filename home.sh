
./shutter.sh
ret=$?
if [ ${RET} -eq 1 ]; then
  echo 'shutter.sh error'
  exit 1
fi

python s3-up.py
ret=$?
if [ ${RET} -eq 1 ]; then
  echo 's3-up.py error'
  exit 1
fi

./line-push.sh
ret=$?
if [ ${RET} -eq 1 ]; then
  echo 'line-push.sh error'
  exit 1
fi

#python_pid=`pgrep -f 'python -m http.server'`
#kill -9 $python_pid
#cd image
#./server.sh &
