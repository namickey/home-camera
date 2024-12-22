num=$(cat tmp.log | grep ${TAG_MAC} | wc -l)

if [[ ${num} -ne "0" ]]; then
  echo 'waka home'
else
  echo 'waka out home'
  ./5.create-stopfile.sh
  ./line-push-papa.sh
  ./line-push-mama.sh
fi
