from machine import Pin, PWM
import time

## Defines
loopCount = 100

class EM:
    def __init__(self):
        servo = PWM(Pin(15))
        servo.freq(50) # 50hz = pulsos de 20 ms
        p0 = Pin(0, Pin.OUT)

    def release_parachute(self):
        for i in range(loopCount):
            p0.high()
            time.sleep(1)
            p0.low()

