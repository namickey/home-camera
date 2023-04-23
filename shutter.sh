python serial_image.py
ret=$?
echo "exit:$ret"
nowdate=`date "+%Y%m%d-%H%M%S"`
cp image/out.jpeg image/all/home-${nowdate}.jpeg
