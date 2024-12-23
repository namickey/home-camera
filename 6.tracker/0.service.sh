
if [ -f "stop-file.txt" ]; then
    echo $(date +"%Y-%m-%d %H:%M:%S") "Stop file exists." | tee -a app.log
    exit 0
fi

echo $(date +"%Y-%m-%d %H:%M:%S") "Starting BLE scan service." | tee -a app.log

sudo ./1.scan_ble.sh

./2.check_log.sh
