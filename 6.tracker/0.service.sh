
if [ -f "stop-file.txt" ]; then
    echo "Stop file exists. Exiting."
    exit 0
fi

echo "Starting BLE scan service."

sudo ./1.scan_ble.sh

./2.check_log.sh
