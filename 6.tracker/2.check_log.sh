num=$(cat tmp.log | grep ${TAG_MAC} | wc -l)

if [[ ${num} -ne "0" ]]; then
  echo 'tracker is home.' | tee -a app.log
else
  echo 'tracker is out of home.' | tee -a app.log
  ./5.create-stopfile.sh
  ./3.line-push-papa.sh
  ./4.line-push-mama.sh
fi
