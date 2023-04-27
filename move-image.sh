#!/bin/bash

# ファイル名に日付及びUUIDを付与して移動
echo 'move-image'
nowdate=`date "+%Y%m%d-%H%M%S"`
uuid=$(< /proc/sys/kernel/random/uuid)
mv image/out.jpeg image/all/home-${nowdate}_${uuid}.jpeg
