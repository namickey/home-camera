import sys
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5.0)

# wait for init
for h in range(50):
    time.sleep(0.1)
    result = ser.read_all()

# send mode
moji='waitbuttonmode\r\n'
print('send')
ser.write(moji.encode('utf-8'))
print('send')

# wait
while True:
    time.sleep(0.5)
    result = ser.read_all()
    if result:
        re = result.decode('utf-8')
        print(re)
        if 'go-home-1-2-3' in re:
            sys.exit(0)
    else:
        print('empty')
