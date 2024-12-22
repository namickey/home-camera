
hciconfig hci0 down
sleep 1

hciconfig hci0 up
sleep 1

sudo hcitool lescan > tmp.log & sleep 20 && sudo pkill --signal SIGINT hcitool

cat tmp.log

hciconfig hci0 down
sleep 1
