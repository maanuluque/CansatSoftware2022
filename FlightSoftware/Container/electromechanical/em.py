from machine import Pin, PWM
import time

## Defines
loopCount = 100

class EM:
    def __init__(self):
        servo = PWM(Pin(15))
        servo.freq(50) # 50hz = pulsos de 20 ms
        p12 = Pin(12, Pin.OUT)
        p13 = Pin(13, Pin.OUT)
        pin0 = Pin(0, Pin.OUT)
        pin1 = Pin(1, Pin.OUT)
        pin2 = Pin(2, Pin.OUT)
        pin3 = Pin(3, Pin.OUT)
        pwm = PWM(pin0)
        pin1.high()
        pin2.low()
        pin3.high()

    def parachute_nicrom_on(self):
        p12.high()
        
    def parachute_nicrom_off(self):
        p12.low()
        
    def payload_nicrom_on(self):
        p13.high()
        
    def payload_nicrom_off(self):
        p13.low()
        
    def start_motor(self):
        pwm.duty_u16(32768)
        
    def stop_motor(self):
        pwm.duty_u16(0)

