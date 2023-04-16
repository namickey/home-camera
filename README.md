# 1. Home Camera to GoogleDrive
自宅のノートパソコン（カメラ付き）で10分毎に撮った写真をGoogleDriveにアップロードして、スマホから閲覧する。  
Laptop + Python3 + CV2 + GoogleDrive + Schedule  

## install
```bash
pip install opencv-python
pip install pydrive
pip install schedule
```

## script
```python
import schedule
import time
import cv2
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint

# 定期実行させたい処理
def job():

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (int(frame.shape[1]/4), int(frame.shape[0]/4))) #サイズ変更
    cv2.imshow('Raw Frame', frame)
    cv2.imwrite('hoge.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() #ブラウザ認証。認証後にcredentials.jsonが作成される。
    drive = GoogleDrive(gauth) #事前にgoogleDriveApiを有効化しておく。
    f = drive.CreateFile({'id':'xxxxxxxxxxxxxxxx', 'mimeType': 'image/jpeg'}) #idを指定して、上書きアップロード
    f.SetContentFile('hoge.jpg')
    f.Upload()
    #pprint.pprint(f) #idが不明な場合は、一度事前にid未指定のままアップロードしてidを確認しておく

def main():
    job()
    # 10分ごとに起動
    schedule.every(10).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == '__main__':
    main()
```

# 2. Home Camera RaspberryPi to Line
自宅のM5StickV(カメラ)及びRaspberryPi4から、Lineへ画像を送信する。

参考  

M5StickC M5StickVを使った簡易監視装置を作ってみる  
https://www.slideshare.net/tomit3/m5stickc-m5stickv  
https://github.com/tomitomi3/SimpleHomeSurveillanceWithM5StickCV  

M5StackでつくるAI機械学習機能搭載インターフォンカメラ  
https://deviceplus.jp/mc-general/m5stack-intercom-camera-1/  

RISC-Vベースの“AIoTカメラ”であるM5StickVをUbuntuで使う  
https://gihyo.jp/admin/serial/01/ubuntu-recipe/0587  

