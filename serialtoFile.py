import serial
import time
import datetime
import struct

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=4.0)
f = open('out.txt', 'a')


while True:
    time.sleep(1.0)
    #result = ser.read(6)
    #print(result)
    #print(struct.unpack('6x', result))
    
    result = ser.read_all()
    if result:
        #minini = datetime.datetime.now().minute
        print(len(result))
        print(type(result))
        #a = result.hex()
        #a = struct.unpack(str(len(result))+'b', result)
        print(result)

    if result == b'\r':    # <Enter>で終了
        break
print('program end')
ser.close()
