from machine import PWM, Pin
import time

pin0 = Pin(0, Pin.OUT)
pin1 = Pin(1, Pin.OUT)
pin2 = Pin(2, Pin.OUT)
pin3 = Pin(3, Pin.OUT)

pwm = PWM(pin0)
pin1.high()
pin2.low()
pin3.high()

maxi = 2**15 - 2

pwm.duty_u16(0)
time.sleep(1)
pin3.low()

