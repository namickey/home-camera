num=$(cat tmp.log | grep ${TAG_MAC} | wc -l)

if [[ ${num} -ne "0" ]]; then
  echo 'tracker is home.' | tee -a app.log
else
  echo 'tracker is out of home.' | tee -a app.log
  ./6.create-stopfile.sh
  touch ./done.txt
  #./4.line-push-papa.sh
  #./5.line-push-mama.sh
fi
