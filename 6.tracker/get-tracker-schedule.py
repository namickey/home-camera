import requests
import datetime

# スケジュールを取得
url = "https://namickey.github.io/home-camera/tracker.json"
response = requests.get(url)
data = response.json()

today = datetime.datetime.today().strftime('%A')
a = [x for x in data["data"]["operating_hours"] if x["day_of_week"] == today]
print(a)
start_time = a[0]["start_time"]
end_time = a[0]["end_time"]

# 現在時刻を取得
current_time = datetime.datetime.now().strftime('%H:%M')

# 判定
if start_time <= current_time <= end_time:
    print("true")
    exit(0)
else:
    print("false")
    exit(1)
