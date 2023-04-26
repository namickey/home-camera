#!/bin/bash

echo 'move-image'
nowdate=`date "+%Y%m%d-%H%M%S"`
uuid=$(< /proc/sys/kernel/random/uuid)
mv image/out.jpeg image/all/home-${nowdate}_${uuid}.jpeg
