from machine import Pin, UART, I2C
import time, utime

def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return Converted

gpsModule = UART(0, baudrate=9600, tx=Pin(19), rx=Pin(18))
buff = bytearray(255)

def get_data():
    print("Running GPS program:")
    while(1):
            gpsModule.readline()
            buff = str(gpsModule.readline())
            parts = buff.split('$')
            #print(buff)
            for data in parts:
                if data != "b'":
                    #print(data)
                    parts2 = data.split(',')
                    if parts2[0] == 'GNGGA' and len(parts2) == 15:
                        #print(data)
                        if(parts2[1] and parts2[2] and parts2[3] and parts2[4] and parts2[5] and parts2[6] and parts2[7] and parts2[9]):
                            latitude = convertToDegree(parts2[2])
                            if (parts2[3] == 'S'):
                                latitude = str(-(float(latitude)))
                            longitude = convertToDegree(parts2[4])
                            if (parts2[5] == 'W'):
                                longitude = str(-(float(longitude)))
                            satellites = parts2[7]
                            GPStime = parts2[1][0:2] + ":" + parts2[1][2:4] + ":" + parts2[1][4:6]
                            altitude = parts2[9]
                            print("Latitude: " + latitude + " Longitude: " + longitude + " Sats: " + satellites + " Time: " + GPStime + " Altitude: " + altitude)
                            return latitude
            time.sleep_ms(1000)