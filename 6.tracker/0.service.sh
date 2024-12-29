# スケジュールを確認する
./1.check-schedule.sh

# 停止ファイルがある場合は終了
if [ -f "stop-file.txt" ]; then
    echo $(date +"%Y-%m-%d %H:%M:%S") "Stop file exists." | tee -a app.log
    exit 0
fi

echo $(date +"%Y-%m-%d %H:%M:%S") "Starting BLE scan service." | tee -a app.log

# BLEスキャンを実行
sudo ./2.scan_ble.sh

# ログを確認し、通知を行う
./3.check_log.sh
