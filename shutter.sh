python shutter.py
ret=$?
if [ ${ret} -eq 1 ]; then
  echo 'shutter.py error'
  exit 1
fi
