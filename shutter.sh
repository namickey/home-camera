python serial_image.py
ret=$?
echo "exit:$ret"
nowdate=`date "+%Y%m%d-%H%M%S"`
uuid=$(< /proc/sys/kernel/random/uuid)
cp image/out.jpeg image/all/home-${nowdate}_${uuid}.jpeg
