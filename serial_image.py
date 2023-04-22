import serial
import time
import datetime

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=4.0)
f = open('out.jpeg', 'wb')

d = ''
i = 0

while True:
    time.sleep(0.1)
    result = ser.read_all()
    re = ''
    if result:
        print('')
        print(len(result))
        #re = str(result).decode('utf-8')
        re = result.decode('utf-8')
        print(re)
        if i > 4:
            #d += str(result).decode('utf-8')
            d += result.decode('utf-8')
        i += 1
    if 'MicroPython' in re:
        break
print('program end')
jpeg = d.splitlines()[0]
print(jpeg)
print('')
print('')

jb = bytes.fromhex(jpeg[0:])
print(jb)
f.write(jb)
f.close()
ser.close()

