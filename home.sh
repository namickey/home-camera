
./shutter.sh
ret=$?
if [ ${RET} -eq 1 ]; then
  echo 'error'
  exit 1
fi

kill -9 `pidof python`

cd image
./server.sh &

