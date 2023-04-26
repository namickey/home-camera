import serial
import time
import datetime

# send mode
#moji='shuttermode\r\n'
#print('send')
#ser.write(moji.encode('utf-8'))
#print('send')

while True:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5.0)
    
    # wait for init
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
        if result:
            re = result.decode('utf-8')
            if 'MicroPython' in re:
                print(re)
                d += re
                result = ser.read_all()
                result = ser.read_all()
                print('print(d)')
                print(d)
                jpeg = d.splitlines()[0]
                if jpeg:
                    if jpeg[0:]:
                        jb = bytes.fromhex(jpeg[0:])
                        f = open('image/out.jpeg', 'wb')
                        f.write(jb)
                        f.close()
                        ser.close()
                        print('shutter done.')
                        break
                d = ''
                i = 0
            print(re)
            d += re
    print('new serial.')