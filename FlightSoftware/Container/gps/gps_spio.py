from machine import Pin, UART
from rp2 import PIO, StateMachine, asm_pio

UART_BAUD = 9600
LENG = 400
PIO_RX_PIN = Pin(19, Pin.IN, Pin.PULL_UP)

@asm_pio(
    autopush=True,
    push_thresh=8,
    in_shiftdir=PIO.SHIFT_RIGHT,
    fifo_join=PIO.JOIN_RX,
)
def uart_rx():
    wait(0, pin, 0)
    set(x, 7)                 [10]
    label("bitloop")
    in_(pins, 1)
    jmp(x_dec, "bitloop")     [6]


def handler(sm):
    print("break", time.ticks_ms(), end=" ")

sm = StateMachine(
    0,
    uart_rx,
    freq=8 * UART_BAUD,
    in_base=PIO_RX_PIN,  # For WAIT, IN
    jmp_pin=PIO_RX_PIN,  # For JMP
)
sm.irq(handler)
sm.active(1)

def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return Converted

def get_nmea():
    gps_data = ""
    #print(len(bin(sm.get()).replace('0b', '')))
    for i in range(LENG):
        gps_data+=(chr(sm.get() >> 24))
    #print(gps_data)
    #print()
    return get_gps_data(gps_data)

def get_gps_data(nmea_msg):
    parts = nmea_msg.split('$')
    #print(buff)
    for data in parts:
        if data != "b'":
            #print(data)
            parts2 = data.split(',')
            if parts2[0] == 'GNGGA' and len(parts2) == 15:
                #print(data)
                if(parts2[1] and parts2[2] and parts2[3] and parts2[4] and parts2[5] and parts2[6] and parts2[7] and parts2[9]):
                    #print("GOT message.")
                    latitude = convertToDegree(parts2[2])
                    if (parts2[3] == 'S'):
                        latitude = str(-(float(latitude)))
                    longitude = convertToDegree(parts2[4])
                    if (parts2[5] == 'W'):
                        longitude = str(-(float(longitude)))
                    satellites = parts2[7]
                    GPStime = parts2[1][0:2] + ":" + parts2[1][2:4] + ":" + parts2[1][4:6]
                    altitude = parts2[9]
                    #print("Latitude: " + latitude + " Longitude: " + longitude + " Sats: " + satellites + " Time: " + GPStime + " Altitude: " + altitude)
                    return (latitude, longitude, satellites, GPStime, altitude)
    else:
        return None


