#!/bin/bash

while true
do
    FILE="image/out.jpeg"
    if [ -e $FILE ]; then
        # 移動
        ./move-image.sh
        # S3へアップロード
        python s3up.py
        # 送信
        ./line-push.sh
    fi
    sleep 1
done
