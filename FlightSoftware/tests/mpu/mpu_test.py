import machine
from time import sleep_ms
from mpu9250 import MPU9250

i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))
sensor = MPU9250(i2c)

while True:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.magnetic)
    print(sensor.temperature)
    sleep_ms(1000)