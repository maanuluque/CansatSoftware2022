from machine import Pin, PWM
import time

## Defines
SIGNAL_TIME = 1

class EM:
    def __init__(self):
        servo = PWM(Pin(15))
        servo.freq(50) # 50hz = pulsos de 20 ms
        #p1 = Pin(0, Pin.OUT)
        #p2 = Pin(2, Pin.OUT)

# me permite defnir cuanto va a durar el estado alto del pulso
# servo.duty_ms()

    def release_parachute(self, parachute_number):
        if parachute_number == 1:
            p0.value(1)
            sleep(SIGNAL_TIME)
            p0.value(0)
        elif parachute_number == 2:
            p1.value(1)
            sleep(SIGNAL_TIME)
            p1.value(0)

#while True:
#    # posicion 0
#    servo.duty_ms(500000)
#    sleep_ms(500)
#    # 90 grados
#    servo.duty_ms(1500000)
#    sleep_ms(500)
#    # 180 grados
#    servo.duty_ms(2500000)
#    sleep_ms(500)
#    servo.duty_ms(1500000)
#    sleep_ms(500)
