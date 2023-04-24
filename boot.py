import image, sensor
#import lcd
from pmu import axp192
#lcd.init()
#lcd.rotation(2)
time.sleep(0.1)

#電源管理
pmu = axp192()
pmu.setScreenBrightness(10) # 8だとちらつく
time.sleep(0.2)

while 1:
	try:
		time.sleep(0.01)
		sensor.reset()
		break
	except:
		time.sleep(0.01)
		continue

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) #QVGA=320x240
sensor.run(1)
time.sleep(0.5)

#カメラから画像取得
img_org = sensor.snapshot()

#加工前にコピー 送信用に加工
img_buf = img_org.copy()
img_buf = img_buf.resize(240,160)
img_buf.compress(quality=50)

#確認用に表示 カメラの比率
#img_org.draw_string(50,50, "home", color=(255,0,0), scale=2, mono_space=False)
#lcd.display(img_org)

#print('img_buf:dir:')
#print(dir(img_buf))
#print('img_buf.to_bytes().sise():')
aa= img_buf.to_bytes()
#print(len(aa))
#print('img_buf.to_bytes():')
bb = ''.join(['{:02x}'.format(b) for b in aa])
#print(len(bb))
print(bb)
sys.exit()
