import serial
import time
import datetime

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5.0)

d = ''
i = 0

for h in range(100):
    #print(h)
    time.sleep(0.1)
    result = ser.read_all()
    re = ''
    if result:
        #print('')
        #print(len(result))
        #re = str(result).decode('utf-8')
        re = result.decode('utf-8')
        print(re)
        if i > 4:
            #d += str(result).decode('utf-8')
            d += result.decode('utf-8')
        i += 1
    if 'MicroPython' in re:
        break

jpeg = d.splitlines()[0]
#print('jpeg')
#print(jpeg)
if jpeg:
    #print(jpeg[0:])
    if jpeg[0:]:
        jb = bytes.fromhex(jpeg[0:])
        f = open('image/out.jpeg', 'wb')
        f.write(jb)
        f.close()
print('program end')
ser.close()