import serial
import time
import datetime

while True:
    # wait for init
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5.0)
    for h in range(50):
        time.sleep(0.1)
        result = ser.read_all()
    
    # shutter
    d = ''
    i = 0
    while True:
        time.sleep(0.1)
        result = ser.read_all()
        re = ''
        # シャッターボタンが押されたら、何度かに分けてデータ受信開始
        if result:
            re = result.decode('utf-8')
            # 写真1枚分の全byteの受信完了後に送られてくる最後の文字列を判定
            if 'MicroPython' in re:
                print(re)
                d += re
                result = ser.read_all()
                result = ser.read_all()
                print(d)
                # jpegと最後の文字列を分離
                jpeg = d.splitlines()[0]
                if jpeg:
                    if jpeg[0:]:
                        # jpegをファイル出力
                        jb = bytes.fromhex(jpeg[0:])
                        f = open('image/out.jpeg', 'wb')
                        f.write(jb)
                        f.close()
                        ser.close()
                        print('shutter done.')
                        break
                d = ''
                i = 0
            # 写真1枚分の全byteを受け取るまでループ
            print(re)
            d += re
    print('new serial.')
