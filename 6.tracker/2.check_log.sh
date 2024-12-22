num=$(cat tmp.log | grep ${bletag_mac} | wc -l)

if [[ ${num} -ne "0" ]]; then
  echo 'waka home'
else
  echo 'waka chia'
  ./line-push-papa.sh
fi
