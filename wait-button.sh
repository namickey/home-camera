
echo "wait"
python wait-button.py
ret=$?
if [ ${ret} -eq 0 ]; then
  exit 0
else
  echo "wait-button.py error"
  exit 1
fi
