# スケジュールを確認する
python get-tracker-schedule.py
if [ ${?} -eq 0 ]; then
    # スケジュール内の場合
    
    if [ -f "done.txt" ]; then
        # 通知済みである場合は、何もしない。
        echo $(date +"%Y-%m-%d %H:%M:%S") "Done file exists." | tee -a app.log
    else
        # まだ通知していない場合は、停止ファイルを削除
        ./7.delete-stopfile.sh
    fi
else
    # スケジュール外の場合は、停止ファイルを作成
    ./6.create-stopfile.sh
    rm -f ./done.txt
fi