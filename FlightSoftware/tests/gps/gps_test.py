from machine import Pin, UART, I2C
import time, utime

gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
#print(gpsModule)
buff = bytearray(255)

print("Running GPS test:")
while(1):
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split('$')
        for data in parts:
            if data != "b'":
                #print(data)
                if data[0] == "GNGLL" or data[0] == "GNGGA":
                    print("Latitude: " + str(data[1]) + '\n')
                    print("Longitude: " + str(data[2]) + '\n')
                    
                   
        time.sleep_ms(1000)