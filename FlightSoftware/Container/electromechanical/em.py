from machine import Pin, PWM
import time

## Defines
loopCount = 100

class EM:
    def __init__(self):
        servo = PWM(Pin(15))
        servo.freq(50) # 50hz = pulsos de 20 ms
        self.p12 = Pin(12, Pin.OUT)
        self.p13 = Pin(13, Pin.OUT)
        
        self.pin1 = Pin(1, Pin.OUT)
        self.pin2 = Pin(2, Pin.OUT)
        self.pin3 = Pin(3, Pin.OUT)
        
        pin0 = Pin(0, Pin.OUT)
        self.pwm0 = PWM(pin0)
        
        pin11 = Pin(11, Pin.OUT)
        self.pwm1 = PWM(pin11)
        
        self.buzzer = False
        
        self.pin1.high()
        self.pin2.low()
        self.pin3.high()

    def parachute_nicrom_on(self):
        self.p12.high()
        
    def parachute_nicrom_off(self):
        self.p12.low()
        
    def payload_nicrom_on(self):
        self.p13.high()
        
    def payload_nicrom_off(self):
        self.p13.low()
        
    def start_motor(self):
        self.pwm0.duty_u16(2**15)
        
    def stop_motor(self):
        self.pwm0.deinit()
        self.pin1.low()
        self.pin3.low()
        
    def start_buzzer(self):
        self.pwm1.freq(2700)
        self.pwm1.duty_u16(32768)
        
    def stop_buzzer(self):
        self.pwm1.deinit()
        
    def toggle_buzzer(self):
        self.buzzer = not self.buzzer
        if (self.buzzer == True):
            self.start_buzzer()
        else:
            self.stop_buzzer()




