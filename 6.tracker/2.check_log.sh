num=$(cat tmp.log | grep ${TAG_MAC} | wc -l)

if [[ ${num} -ne "0" ]]; then
  echo 'tracker is home.'
else
  echo 'tracker is out of home.'
  ./5.create-stopfile.sh
  ./line-push-papa.sh
  ./line-push-mama.sh
fi
