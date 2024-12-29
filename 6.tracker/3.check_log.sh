num=$(cat tmp.log | grep ${TAG_MAC} | wc -l)

if [[ ${num} -ne "0" ]]; then
    # スキャンしたデバイスに指定MACアドレスが存在する場合
    echo 'tracker is home.' | tee -a app.log
else
    # スキャンしたデバイスに指定MACアドレスが存在しない場合
    echo 'tracker is out of home.' | tee -a app.log
    ./6.create-stopfile.sh
    touch ./done.txt
    #./4.line-push-papa.sh
    #./5.line-push-mama.sh
fi
