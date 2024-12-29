python get-tracker-schedule.py
if [ ${?} -eq 0 ]; then
    if [ -f "done.txt" ]; then
        echo $(date +"%Y-%m-%d %H:%M:%S") "Done file exists." | tee -a app.log
    else
        ./7.delete-stopfile.sh
    fi
else
    ./6.create-stopfile.sh
    rm -f ./done.txt
fi