
hciconfig hci0 down
sleep 1
echo "power down"

hciconfig hci0 up
sleep 1
echo "power up"

sudo hcitool lescan > tmp.log & sleep 10 && sudo pkill --signal SIGINT hcitool

cat tmp.log

hciconfig hci0 down
sleep 1
