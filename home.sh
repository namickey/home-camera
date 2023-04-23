
./shutter.sh
ret=$?
if [ ${RET} -eq 1 ]; then
  echo 'error'
  exit 1
fi

python_pid=`pgrep -f 'python -m http.server'`
kill -9 $python_pid

cd image
./server.sh &

