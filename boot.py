import image, sensor
import lcd
from pmu import axp192

lcd.init()
lcd.rotation(2)
time.sleep(0.1)

# LED
from Maix import GPIO
from board import board_info
fm.register(board_info.LED_B, fm.fpioa.GPIO6)

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

# ボタン押下待ち
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
while 1:
	if but_a.value() == 0:
		# LED ON
		led_r = GPIO(GPIO.GPIO6, GPIO.OUT)
		led_r.value(0)

		#カメラから画像取得
		img_org = sensor.snapshot()

		#加工前にコピー 送信用に加工
		img_buf = img_org.copy()
		img_buf = img_buf.resize(240,160)
		img_buf.compress(quality=50)

		#確認用に表示 カメラの比率
		#img_org.draw_string(50,50, "home", color=(255,0,0), scale=2, mono_space=False)
		lcd.display(img_org)

		# LED OFF
		led_r.value(1)

		# 送信
		aa= img_buf.to_bytes()
		bb = ''.join(['{:02x}'.format(b) for b in aa])
		print(bb)
		print('MicroPython')
		# LCD OFF
		time.sleep(3.0)
		lcd.clear()
		sys.exit()
