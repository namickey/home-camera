#!/bin/bash

while true
do
    FILE="image/out.jpeg"
    if [ -e $FILE ]; then
        ./move-image.sh
        python s3up.py
        ./line-push.sh
    fi
    sleep 1
done
